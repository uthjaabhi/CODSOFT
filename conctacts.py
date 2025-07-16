import tkinter as tk
from tkinter import ttk, messagebox

class ContactManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("800x600")
        self.contacts = []
        
        # Custom styling
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', padding=6, font=('Helvetica', 10))
        self.style.map('TButton',
                      foreground=[('active', 'white'), ('!active', 'black')],
                      background=[('active', '#4a6baf'), ('!disabled', '#e1e1e1')])
        
        self.create_widgets()
        self.load_sample_contacts()
        
    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Contact Form
        self.form_frame = ttk.LabelFrame(self.main_frame, text="Contact Details", padding=15)
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Form fields
        ttk.Label(self.form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.form_frame, width=25)
        self.name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(self.form_frame, width=25)
        self.phone_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(self.form_frame, width=25)
        self.email_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(self.form_frame, text="Address:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.address_entry = tk.Text(self.form_frame, width=25, height=4, wrap=tk.WORD)
        self.address_entry.grid(row=3, column=1, pady=5)
        
        # Action buttons
        self.button_frame = ttk.Frame(self.form_frame)
        self.button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.add_button = ttk.Button(self.button_frame, text="Add", command=self.add_contact)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.update_button = ttk.Button(self.button_frame, text="Update", command=self.update_contact)
        self.update_button.pack(side=tk.LEFT, padx=5)
        self.update_button.config(state=tk.DISABLED)
        
        self.clear_button = ttk.Button(self.button_frame, text="Clear", command=self.clear_form)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Right panel - Contact List
        self.list_frame = ttk.LabelFrame(self.main_frame, text="Contact List", padding=15)
        self.list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Search bar
        search_frame = ttk.Frame(self.list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_contacts)
        self.search_button.pack(side=tk.LEFT)
        
        self.reset_button = ttk.Button(search_frame, text="Reset", command=self.reset_search)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Contact list treeview
        self.tree = ttk.Treeview(self.list_frame, columns=("Name", "Phone", "Email"), show="headings")
        
        self.tree.heading("Name", text="Name", command=lambda: self.sort_column("Name", False))
        self.tree.heading("Phone", text="Phone", command=lambda: self.sort_column("Phone", False))
        self.tree.heading("Email", text="Email", command=lambda: self.sort_column("Email", False))
        
        self.tree.column("Name", width=120, anchor=tk.W)
        self.tree.column("Phone", width=100, anchor=tk.W)
        self.tree.column("Email", width=150, anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons for list
        self.action_frame = ttk.Frame(self.list_frame)
        self.action_frame.pack(fill=tk.X, pady=10)
        
        self.delete_button = ttk.Button(self.action_frame, text="Delete", command=self.delete_contact)
        self.delete_button.pack(side=tk.LEFT)
        self.delete_button.config(state=tk.DISABLED)
        
        self.view_button = ttk.Button(self.action_frame, text="View Details", command=self.view_contact)
        self.view_button.pack(side=tk.LEFT, padx=5)
        self.view_button.config(state=tk.DISABLED)
        
        # Bind tree selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.search_entry.bind("<Return>", lambda event: self.search_contacts())
        
    def load_sample_contacts(self):
        sample_contacts = [
            {"name": "John Doe", "phone": "555-1234", "email": "john@example.com", "address": "123 Main St, City"},
            {"name": "Jane Smith", "phone": "555-5678", "email": "jane@example.com", "address": "456 Oak Ave, Town"},
            {"name": "Robert Johnson", "phone": "555-9012", "email": "robert@example.com", "address": "789 Pine Rd, Village"}
        ]
        for contact in sample_contacts:
            self.contacts.append(contact)
        self.update_treeview()
        
    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for contact in sorted(self.contacts, key=lambda x: x['name']):
            self.tree.insert("", tk.END, values=(
                contact["name"],
                contact["phone"],
                contact["email"]
            ))
    
    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get("1.0", tk.END).strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter a name")
            return
            
        if any(c['name'].lower() == name.lower() for c in self.contacts):
            messagebox.showwarning("Warning", "A contact with this name already exists")
            return
            
        new_contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }
        
        self.contacts.append(new_contact)
        self.update_treeview()
        self.clear_form()
        messagebox.showinfo("Success", "Contact added successfully")
    
    def update_contact(self):
        selected = self.get_selected_contact()
        if not selected:
            return
            
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get("1.0", tk.END).strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter a name")
            return
            
        # Check if new name conflicts with another contact
        for contact in self.contacts:
            if contact['name'].lower() == name.lower() and contact != selected:
                messagebox.showwarning("Warning", "Another contact with this name already exists")
                return
        
        selected.update({
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        })
        
        self.update_treeview()
        self.clear_form()
        messagebox.showinfo("Success", "Contact updated successfully")
    
    def delete_contact(self):
        selected = self.get_selected_contact()
        if not selected:
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            self.contacts.remove(selected)
            self.update_treeview()
            self.clear_form()
            messagebox.showinfo("Success", "Contact deleted successfully")
    
    def view_contact(self):
        selected = self.get_selected_contact()
        if not selected:
            return
            
        details = f"Name: {selected['name']}\n"
        details += f"Phone: {selected['phone']}\n"
        details += f"Email: {selected['email']}\n"
        details += f"Address:\n{selected['address']}"
        
        messagebox.showinfo("Contact Details", details)
    
    def search_contacts(self):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            self.update_treeview()
            return
            
        filtered = []
        for contact in self.contacts:
            if (search_term in contact['name'].lower() or 
                search_term in contact['phone'].lower() or
                search_term in contact['email'].lower() or
                search_term in contact['address'].lower()):
                filtered.append(contact)
                
        self.tree.delete(*self.tree.get_children())
        for contact in filtered:
            self.tree.insert("", tk.END, values=(
                contact["name"],
                contact["phone"],
                contact["email"]
            ))
            
    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.update_treeview()
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete("1.0", tk.END)
        self.update_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.view_button.config(state=tk.DISABLED)
        self.add_button.config(state=tk.NORMAL)
        
    def get_selected_contact(self):
        selected_item = self.tree.focus()
        if not selected_item:
            return None
            
        selected_values = self.tree.item(selected_item)['values']
        if not selected_values:
            return None
            
        name = selected_values[0]
        for contact in self.contacts:
            if contact['name'] == name:
                return contact
        return None
    
    def on_tree_select(self, event):
        selected = self.get_selected_contact()
        if selected:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, selected['name'])
            
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, selected['phone'])
            
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, selected['email'])
            
            self.address_entry.delete("1.0", tk.END)
            self.address_entry.insert("1.0", selected['address'])
            
            self.update_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            self.view_button.config(state=tk.NORMAL)
            self.add_button.config(state=tk.DISABLED)
    
    def sort_column(self, col, reverse):
        contacts = [(self.tree.set(child, col).lower(), child) for child in self.tree.get_children('')]
        contacts.sort(reverse=reverse)
        
        for index, (val, child) in enumerate(contacts):
            self.tree.move(child, '', index)
            
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerGUI(root)
    root.mainloop()
