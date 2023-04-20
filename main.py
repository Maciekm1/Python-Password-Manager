from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)

    password = "".join(password_list)

    # Copy password to clipboard when generated
    pyperclip.copy(password)

    password_entry.delete(0, END)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    pw = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": pw
        }
    }

    if len(website) < 1 or len(username) < 1 or len(pw) < 1:
        messagebox.showwarning(title="No Input Detected", message="Please don't leave any empty boxes!")
        return

    is_okay = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {username} "
                                                            f"\nPassword: {pw} \nIs it ok to save?")
    if is_okay:

        try:
            with open("data.json", "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)

        else:
            data.update(new_data)

            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- Website Search ------------------------------- #
def website_search():
    website = website_entry.get()

    try:
        with open("data.json", "r") as json_data:
            data_dict = json.load(json_data)
    except FileNotFoundError:
        messagebox.showerror(title="No file found", message=f"Unable to find ./data.json filepath")
    else:
        for (website_name, data) in data_dict.items():
            if website_name.lower() == website.lower():
                username = data["username"]
                password = data["password"]
                messagebox.showinfo(message=f"username: {username}\npassword: {password}\n\nPassword copied to "
                                            f"clipboard.",
                                    title=f"{website_name.title()}")
                pyperclip.copy(password)
            else:
                messagebox.showwarning(message=f"No info for {website_entry.get()} found.",
                                       title=f"No Data Found")


# ---------------------------- UI SETUP ------------------------------- #
canvas = Canvas(width=200, height=200, highlightthickness=0)

logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Website
website_label = Label(text="Website:")
website_label.grid(column=0, row=1, sticky="E")

website_entry = Entry()
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=1, sticky="WE")

# Website Search Key
website_search_button = Button(text="Search", command=website_search)
website_search_button.grid(column=2, row=1, sticky="WE")

# Username
username_label = Label(text="Email/Username")
username_label.grid(column=0, row=2, sticky="E")

username_entry = Entry()
username_entry.grid(column=1, row=2, columnspan=2, sticky="WE")
username_entry.insert(0, "maciekm1pro@gmail.com")

# Password
password_label = Label(text="Password")
password_label.grid(column=0, row=3, sticky="E")

password_entry = Entry()
password_entry.grid(column=1, row=3, columnspan=1, sticky="WE")

# Buttons
add_button = Button(text="Add", width=35, command=save_password)
add_button.grid(column=1, row=4, columnspan=2, sticky="WE")

generate_password_button = Button(text="Generate Password", width=15, command=generate_password)
generate_password_button.grid(column=2, row=3, sticky="W")

window.mainloop()
