import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os

DATA_FILE = "patients.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class PatientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Health Record System (GUI)")
        self.root.geometry("900x520")
        self.root.resizable(False, False)

        self.data = load_data()

        self.create_widgets()
        self.refresh_listbox()

    def create_widgets(self):
        # Left frame: form
        frm_left = ttk.Frame(self.root, padding=12)
        frm_left.place(x=10, y=10, width=420, height=500)

        ttk.Label(frm_left, text="Patient ID:").grid(row=0, column=0, sticky="w")
        self.ent_id = ttk.Entry(frm_left)
        self.ent_id.grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(frm_left, text="Name:").grid(row=1, column=0, sticky="w")
        self.ent_name = ttk.Entry(frm_left)
        self.ent_name.grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Label(frm_left, text="Age:").grid(row=2, column=0, sticky="w")
        self.ent_age = ttk.Entry(frm_left)
        self.ent_age.grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Label(frm_left, text="Disease / Symptoms:").grid(row=3, column=0, sticky="w")
        self.ent_disease = ttk.Entry(frm_left)
        self.ent_disease.grid(row=3, column=1, sticky="ew", pady=6)

        ttk.Label(frm_left, text="Diagnosis:").grid(row=4, column=0, sticky="w")
        self.ent_diagnosis = ttk.Entry(frm_left)
        self.ent_diagnosis.grid(row=4, column=1, sticky="ew", pady=6)

        ttk.Label(frm_left, text="Medicines:").grid(row=5, column=0, sticky="w")
        self.ent_medicines = ttk.Entry(frm_left)
        self.ent_medicines.grid(row=5, column=1, sticky="ew", pady=6)

        # Make columns expand correctly
        frm_left.columnconfigure(1, weight=1)

        # Buttons
        btn_frame = ttk.Frame(frm_left)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=12, sticky="ew")
        btn_frame.columnconfigure((0,1,2), weight=1)

        self.btn_add = ttk.Button(btn_frame, text="Add Patient", command=self.add_patient)
        self.btn_add.grid(row=0, column=0, padx=4, sticky="ew")

        self.btn_update = ttk.Button(btn_frame, text="Update Patient", command=self.update_patient)
        self.btn_update.grid(row=0, column=1, padx=4, sticky="ew")

        self.btn_delete = ttk.Button(btn_frame, text="Delete Patient", command=self.delete_patient)
        self.btn_delete.grid(row=0, column=2, padx=4, sticky="ew")

        # Lower buttons
        lower_frame = ttk.Frame(frm_left)
        lower_frame.grid(row=7, column=0, columnspan=2, pady=4, sticky="ew")
        lower_frame.columnconfigure((0,1,2), weight=1)

        self.btn_search = ttk.Button(lower_frame, text="Search", command=self.search_patient)
        self.btn_search.grid(row=0, column=0, padx=4, sticky="ew")

        self.btn_export = ttk.Button(lower_frame, text="Export Report", command=self.export_report)
        self.btn_export.grid(row=0, column=1, padx=4, sticky="ew")

        self.btn_clear = ttk.Button(lower_frame, text="Clear Fields", command=self.clear_fields)
        self.btn_clear.grid(row=0, column=2, padx=4, sticky="ew")

        # Right frame: list of patients and details
        frm_right = ttk.Frame(self.root, padding=12)
        frm_right.place(x=440, y=10, width=450, height=500)

        ttk.Label(frm_right, text="Patients List:").pack(anchor="w")
        self.listbox = tk.Listbox(frm_right, height=20, activestyle="none")
        self.listbox.pack(fill="both", expand=True, pady=6)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # A small details box
        ttk.Label(frm_right, text="Selected Patient Details:").pack(anchor="w", pady=(8,0))
        self.txt_details = tk.Text(frm_right, height=8, state="disabled", wrap="word")
        self.txt_details.pack(fill="both", expand=False, pady=6)

        # Search entry on top-right for quick filtering
        search_frame = ttk.Frame(frm_right)
        search_frame.pack(fill="x", pady=(6,0))
        ttk.Label(search_frame, text="Quick filter (name/id):").pack(side="left")
        self.ent_quick = ttk.Entry(search_frame)
        self.ent_quick.pack(side="left", fill="x", expand=True, padx=6)
        self.ent_quick.bind("<KeyRelease>", self.on_quick_filter)

    def refresh_listbox(self, filter_text=""):
        self.listbox.delete(0, tk.END)
        for p in self.data:
            display = f"{p['id']} — {p['name']} ({p.get('age','')})"
            if filter_text:
                if filter_text.lower() in display.lower():
                    self.listbox.insert(tk.END, display)
            else:
                self.listbox.insert(tk.END, display)
        self.clear_details_box()

    def on_quick_filter(self, event=None):
        txt = self.ent_quick.get().strip()
        self.refresh_listbox(filter_text=txt)

    def on_select(self, event):
        if not self.listbox.curselection():
            return
        idx = self.listbox.curselection()[0]
        # The listbox shows filtered view; find the matching item by parsing id
        selection_text = self.listbox.get(idx)
        pid = selection_text.split("—")[0].strip()
        patient = self.find_patient_by_id(pid)
        if patient:
            self.populate_fields(patient)
            self.show_details(patient)

    def find_patient_by_id(self, pid):
        for p in self.data:
            if p["id"] == pid:
                return p
        return None

    def populate_fields(self, p):
        self.ent_id.delete(0, tk.END); self.ent_id.insert(0, p["id"])
        self.ent_name.delete(0, tk.END); self.ent_name.insert(0, p["name"])
        self.ent_age.delete(0, tk.END); self.ent_age.insert(0, p.get("age",""))
        self.ent_disease.delete(0, tk.END); self.ent_disease.insert(0, p.get("disease",""))
        self.ent_diagnosis.delete(0, tk.END); self.ent_diagnosis.insert(0, p.get("diagnosis",""))
        self.ent_medicines.delete(0, tk.END); self.ent_medicines.insert(0, p.get("medicines",""))

    def show_details(self, p):
        self.txt_details.config(state="normal")
        self.txt_details.delete("1.0", tk.END)
        lines = [
            f"ID: {p['id']}",
            f"Name: {p['name']}",
            f"Age: {p.get('age','')}",
            f"Disease/Symptoms: {p.get('disease','')}",
            f"Diagnosis: {p.get('diagnosis','')}",
            f"Medicines: {p.get('medicines','')}",
        ]
        self.txt_details.insert(tk.END, "\n".join(lines))
        self.txt_details.config(state="disabled")

    def clear_details_box(self):
        self.txt_details.config(state="normal")
        self.txt_details.delete("1.0", tk.END)
        self.txt_details.config(state="disabled")

    def clear_fields(self):
        self.ent_id.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_age.delete(0, tk.END)
        self.ent_disease.delete(0, tk.END)
        self.ent_diagnosis.delete(0, tk.END)
        self.ent_medicines.delete(0, tk.END)
        self.listbox.selection_clear(0, tk.END)

    def add_patient(self):
        pid = self.ent_id.get().strip()
        name = self.ent_name.get().strip()
        age = self.ent_age.get().strip()
        disease = self.ent_disease.get().strip()
        diagnosis = self.ent_diagnosis.get().strip()
        medicines = self.ent_medicines.get().strip()

        if not pid or not name:
            messagebox.showwarning("Missing info", "Patient ID and Name are required.")
            return

        if self.find_patient_by_id(pid):
            messagebox.showerror("Duplicate ID", "A patient with this ID already exists.")
            return

        new_p = {
            "id": pid,
            "name": name,
            "age": age,
            "disease": disease,
            "diagnosis": diagnosis,
            "medicines": medicines
        }
        self.data.append(new_p)
        save_data(self.data)
        self.refresh_listbox()
        messagebox.showinfo("Success", "Patient added successfully.")
        self.clear_fields()

    def search_patient(self):
        keyword = simpledialog.askstring("Search", "Enter Patient ID or Name to search:")
        if not keyword:
            return
        keyword = keyword.strip().lower()
        results = [p for p in self.data if p["id"].lower() == keyword or p["name"].lower() == keyword]
        if not results:
            # partial match by name
            results = [p for p in self.data if keyword in p["name"].lower() or keyword in p["id"].lower()]

        if not results:
            messagebox.showinfo("Not found", "No patient found with that ID or name.")
            return

        # If multiple results, ask user to choose
        if len(results) > 1:
            options = [f"{p['id']} — {p['name']}" for p in results]
            choice = simpledialog.askinteger("Multiple results",
                                             "Multiple patients found.\nChoose index (starting 1):\n" +
                                             "\n".join(f"{i+1}. {opt}" for i,opt in enumerate(options)),
                                             minvalue=1, maxvalue=len(options))
            if not choice:
                return
            patient = results[choice-1]
        else:
            patient = results[0]

        # select the patient in listbox and populate
        self.populate_fields(patient)
        self.show_details(patient)
        # Try to select the item in the listbox (refresh to ensure present)
        self.refresh_listbox(filter_text=self.ent_quick.get().strip())
        # Find index
        for i in range(self.listbox.size()):
            if self.listbox.get(i).startswith(patient['id']):
                self.listbox.select_set(i)
                self.listbox.see(i)
                break

    def update_patient(self):
        pid = self.ent_id.get().strip()
        if not pid:
            messagebox.showwarning("Missing ID", "Enter Patient ID to update.")
            return

        patient = self.find_patient_by_id(pid)
        if not patient:
            messagebox.showerror("Not found", "No patient found with that ID.")
            return

        # Confirm
        if not messagebox.askyesno("Confirm", f"Update patient {pid}?"):
            return

        patient['name'] = self.ent_name.get().strip() or patient['name']
        patient['age'] = self.ent_age.get().strip() or patient.get('age','')
        patient['disease'] = self.ent_disease.get().strip() or patient.get('disease','')
        patient['diagnosis'] = self.ent_diagnosis.get().strip() or patient.get('diagnosis','')
        patient['medicines'] = self.ent_medicines.get().strip() or patient.get('medicines','')

        save_data(self.data)
        self.refresh_listbox(filter_text=self.ent_quick.get().strip())
        messagebox.showinfo("Updated", "Patient record updated successfully.")

    def delete_patient(self):
        pid = self.ent_id.get().strip()
        if not pid:
            messagebox.showwarning("Missing ID", "Enter Patient ID to delete.")
            return

        if not self.find_patient_by_id(pid):
            messagebox.showerror("Not found", "No patient found with that ID.")
            return

        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently delete patient {pid}?"):
            return

        self.data = [p for p in self.data if p["id"] != pid]
        save_data(self.data)
        self.refresh_listbox(filter_text=self.ent_quick.get().strip())
        self.clear_fields()
        messagebox.showinfo("Deleted", "Patient deleted successfully.")

    def export_report(self):
        pid = self.ent_id.get().strip()
        if not pid:
            messagebox.showwarning("Missing ID", "Enter Patient ID to export report.")
            return
        p = self.find_patient_by_id(pid)
        if not p:
            messagebox.showerror("Not found", "No patient found with that ID.")
            return

        # Ask where to save
        initial = f"report_{pid}.txt"
        file_path = filedialog.asksaveasfilename(title="Save report as", defaultextension=".txt",
                                                 initialfile=initial,
                                                 filetypes=[("Text files","*.txt"), ("All files","*.*")])
        if not file_path:
            return

        try:
            with open(file_path, "w") as f:
                f.write("------ Patient Report ------\n")
                f.write(f"ID: {p['id']}\n")
                f.write(f"Name: {p['name']}\n")
                f.write(f"Age: {p.get('age','')}\n")
                f.write(f"Disease: {p.get('disease','')}\n")
                f.write(f"Diagnosis: {p.get('diagnosis','')}\n")
                f.write(f"Medicines: {p.get('medicines','')}\n")
            messagebox.showinfo("Saved", f"Report saved as:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PatientApp(root)
    root.mainloop()
