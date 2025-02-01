import pandas as pd
from app import ClickTracking, db

def generate_report():
    data = ClickTracking.query.all()
    report_data = [{"User": d.user, "Reason": d.reason} for d in data]
    df = pd.DataFrame(report_data)
    df.to_csv("report.csv", index=False)
    print("Your report is generated! : report.csv")

if __name__ == "__main__":
    generate_report()