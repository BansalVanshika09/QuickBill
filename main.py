import pandas as pd

class UserManager:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.load_data()

    def load_data(self):
        """Load user data from the Excel file."""
        try:
            self.df = pd.read_excel(self.excel_file)
            print("User  data loaded successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = pd.DataFrame(columns=["User  ID", "Name", "Email"])

    def save_data(self):
        """Save user data back to the Excel file."""
        try:
            self.df.to_excel(self.excel_file, index=False)
            print("User  data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_user(self, user_id, name, email):
        """Add a new user to the DataFrame."""
        new_user = pd.DataFrame([[user_id, name, email]], columns=["User  ID", "Name", "Email"])
        self.df = pd.concat([self.df, new_user], ignore_index=True)
        self.save_data()

    def update_user(self, user_id, name=None, email=None):
        """Update an existing user's information."""
        user_index = self.df[self.df['User  ID'] == user_id].index
        if not user_index.empty:
            if name:
                self.df.at[user_index[0], 'Name'] = name
            if email:
                self.df.at[user_index[0], 'Email'] = email
            self.save_data()
        else:
            print("User  not found.")

    def get_user(self, user_id):
        """Retrieve user information by User ID."""
        user = self.df[self.df['User  ID'] == user_id]
        if not user.empty:
            return user.iloc[0].to_dict()
        else:
            print("User  not found.")
            return None