"""
routes.py — VitalsDemo-sovelluksen URL-reitit.
"""

import re

from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user

import models

main_bp = Blueprint("main", __name__)

# Validointirajat (ks. vaatimusmäärittely, kohta 6)
VALID_RANGES = {
    "HR": (20, 300),
    "SpO2": (50, 100),
    "RR": (4, 60),
    "TEMP": (30.0, 45.0),
}
UNITS = {"HR": "bpm", "SpO2": "%", "RR": "/min", "TEMP": "°C", "NIBP": "mmHg"}
NIBP_RE = re.compile(r"^(\d{2,3})/(\d{2,3})$")


def validate_measurement(param_type, value):
    """Palauttaa virheviestin tai None, jos arvo on kelvollinen."""
    if param_type == "NIBP":
        match = NIBP_RE.match(value)
        if not match:
            return 'NIBP-arvon on oltava muodossa "120/80".'
        sys_val, dia_val = int(match.group(1)), int(match.group(2))
        if not (60 <= sys_val <= 250):
            return "Systolisen paineen on oltava välillä 60–250 mmHg."
        if not (30 <= dia_val <= 150):
            return "Diastolisen paineen on oltava välillä 30–150 mmHg."
        return None

    if param_type not in VALID_RANGES:
        return "Tuntematon parametrityyppi."

    try:
        number = float(value)
    except (TypeError, ValueError):
        return "Arvon on oltava numero."

    low, high = VALID_RANGES[param_type]
    if not (low <= number <= high):
        return f"Arvon on oltava välillä {low}–{high}."
    return None


@main_bp.route("/")
@login_required
def index():
    return redirect(url_for("main.patients_list"))


@main_bp.route("/patients")
@login_required
def patients_list():
    patients = models.get_all_patients_with_latest()
    stats = None
    if current_user.role == "laakari":
        raw_stats = models.get_user_stats()
        usernames = sorted(set(raw_stats["measurements"]) | set(raw_stats["notes"]))
        stats = [
            {
                "username": username,
                "measurements": raw_stats["measurements"].get(username, 0),
                "notes": raw_stats["notes"].get(username, 0),
            }
            for username in usernames
        ]
    return render_template("patients.html", patients=patients, stats=stats)


@main_bp.route("/patients/add", methods=["GET", "POST"])
@login_required
def add_patient():
    if current_user.role != "laakari":
        abort(403)

    error = None
    if request.method == "POST":
        name = request.form.get("patient-name", "").strip()
        dob = request.form.get("patient-dob", "").strip()
        room = request.form.get("patient-room", "").strip()

        if not name:
            error = "Nimi on pakollinen."
        else:
            patient_id = models.create_patient(name, dob, room)
            return redirect(url_for("main.patient_detail", patient_id=patient_id))

    return render_template("add_patient.html", error=error)


@main_bp.route("/patients/<int:patient_id>")
@login_required
def patient_detail(patient_id):
    patient = models.get_patient(patient_id)
    if patient is None:
        abort(404)

    measurements = models.get_measurements_for_patient(patient_id)
    notes = models.get_notes_for_patient(patient_id)
    return render_template(
        "patient_detail.html", patient=patient, measurements=measurements, notes=notes
    )


@main_bp.route("/patients/<int:patient_id>/measurements/add", methods=["GET", "POST"])
@login_required
def add_measurement(patient_id):
    patient = models.get_patient(patient_id)
    if patient is None:
        abort(404)

    error = None
    if request.method == "POST":
        param_type = request.form.get("param-type", "")
        value = request.form.get("value", "").strip()
        error = validate_measurement(param_type, value)

        if error is None:
            unit = UNITS.get(param_type, "")
            models.create_measurement(
                patient_id, param_type, value, unit, current_user.username
            )
            return redirect(url_for("main.patient_detail", patient_id=patient_id))

    return render_template("add_measurement.html", patient=patient, error=error)


@main_bp.route("/patients/<int:patient_id>/notes/add", methods=["POST"])
@login_required
def add_note(patient_id):
    if current_user.role != "laakari":
        abort(403)

    patient = models.get_patient(patient_id)
    if patient is None:
        abort(404)

    content = request.form.get("note-content", "").strip()
    if content:
        models.create_note(patient_id, content, current_user.username)

    return redirect(url_for("main.patient_detail", patient_id=patient_id))


@main_bp.route("/patients/<int:patient_id>/delete", methods=["POST"])
@login_required
def delete_patient_route(patient_id):
    if current_user.role != "laakari":
        abort(403)

    patient = models.get_patient(patient_id)
    if patient is None:
        abort(404)

    models.delete_patient(patient_id)
    return redirect(url_for("main.patients_list"))


@main_bp.app_errorhandler(403)
def forbidden(_error):
    return render_template("403.html"), 403
