import csv
import os

class Feedback:
    def __init__(self, service_name, comment, rating):
        self.service_name = service_name
        self.comment = comment
        self.rating = rating

    def save_to_csv(self, file_path="feedback.csv"):
        # Create CSV file with headers if it does not exist
        if not os.path.exists(file_path):
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Service Name", "Comment", "Rating"])

        # Append the feedback
        with open(file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([self.service_name, self.comment, self.rating])

#example usage:
feedback = Feedback("Car Washing", "Great service!", 5)
feedback.save_to_csv()