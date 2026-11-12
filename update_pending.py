
from app import generate_health_remarks
from database import get_connection

def update_pending_records():
    conn = get_connection()

    patients = conn.execute("""
        SELECT id, full_name, glucose, haemoglobin, cholesterol
        FROM patients
        WHERE remarks = 'Pending AI analysis'
        ORDER BY id
    """).fetchall()

    print(f"Found {len(patients)} pending records.")

    for patient in patients:
        print(f"\nProcessing ID {patient['id']}: {patient['full_name']}")

        try:
            remarks = generate_health_remarks(
                patient["glucose"],
                patient["haemoglobin"],
                patient["cholesterol"]
            )

            conn.execute("""
                UPDATE patients
                SET remarks = ?
                WHERE id = ?
            """, (remarks, patient["id"]))

            conn.commit()
            print("SUCCESS: AI remarks saved.")

        except Exception as error:
            print(f"FAILED: {error}")

    conn.close()
    print("\nUpdate process finished.")


if __name__ == "__main__":
    update_pending_records()
