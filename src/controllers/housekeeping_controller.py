from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db_connection
from models.housekeeping import Housekeeping


housekeeping_bp = Blueprint("housekeeping", __name__, url_prefix="/housekeeping")

@housekeeping_bp.route("/")
def housekeeping():
    return render_template("housekeeping.html")

@housekeeping_bp.route("/new",methods=["POST"])
def new_housekeeping():
    hk = Housekeeping(
        type=request.form["Hktype"],
        notes=request.form.get("notes"),
        name=request.form["fullName"],
        phone=request.form["phone"],
        email=request.form["email"],
        date=request.form["date"],
        price=150
    )

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO housekeeping_requests1
        (type, notes, name, phone, email, date, price)
        OUTPUT INSERTED.id
        VALUES (?,?,?,?,?,?,?);      
    """, (
        hk.type,
        hk.notes,
        hk.name,
        hk.phone,
        hk.email,
        hk.date,
        hk.price
    ))

    
    request_id = cursor.fetchone()[0]
    conn.commit()


    cursor.close()
    conn.close()


    return redirect(url_for("housekeeping.payment", request_id=request_id))



@housekeeping_bp.route("/payment/<int:request_id>", methods=["GET", "POST"])
def payment(request_id):
    print("Payment route hit with ID:", request_id)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM dbo.housekeeping_requests1 WHERE id = ?",
        (request_id,)
    )
    #order = cursor.fetchone()

    row = cursor.fetchone()
 

    order = None
    if row:
        columns = [column[0] for column in cursor.description]
        order = dict(zip(columns, row))


    cursor.close()
    conn.close()

    return render_template("Payment.html", order=order)


@housekeeping_bp.route("/confirmation/", methods=["GET", "POST"])
def confirmation():
    return render_template("Confirmation.html")