import tkinter as tk
import requests

def get_medicine_info(event=None):
    medicine_name = medicine_name_entry.get()
    response = requests.get(f"https://api.fda.gov/drug/label.json?search={medicine_name}")
    if response.status_code == 200:
        response_json = response.json()
        results = response_json.get("results", [])
        if len(results) > 0:
            medicine_info = results[0]
            info_text.delete('1.0', tk.END) 
            info_text.insert(tk.END, f"Here is the information for {medicine_name}:\n\n")
            info_text.insert(tk.END, f"Manufacturer: {medicine_info.get('openfda', {}).get('manufacturer_name', ['Unknown'])[0]}\n\n")
            info_text.insert(tk.END, f"Indications and Usage: {medicine_info.get('indications_and_usage', 'Not available')}\n\n")
            info_text.insert(tk.END, f"Dosage and Administration: {medicine_info.get('dosage_and_administration', 'Not available')}\n\n")
            info_text.insert(tk.END, f"Active Ingredient(s): {', '.join(medicine_info.get('active_ingredient', ['Unknown']))}\n\n")
            info_text.insert(tk.END, f"Possible Side Effects: {medicine_info.get('adverse_reactions', 'Not available')}\n\n")
           
        else:
            info_text.delete('1.0', tk.END) 
            info_text.insert(tk.END, f"No information found for {medicine_name}.")
    else:
        info_text.delete('1.0', tk.END) 
        info_text.insert(tk.END, f"Error: {response.status_code} - {response.reason}")

root = tk.Tk()
root.title('MedInfo')
root.geometry('900x500')

input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, padx=10, pady=10)

medicine_name_label = tk.Label(input_frame, text="Enter the name of the medicine:")
medicine_name_label.pack(side=tk.LEFT)
medicine_name_entry = tk.Entry(input_frame)
medicine_name_entry.pack(side=tk.LEFT, padx=5)
medicine_name_entry.bind("<Return>", get_medicine_info)

get_info_button = tk.Button(root, text="Get Information", command=get_medicine_info)
get_info_button.pack(pady=5)

info_text = tk.Text(root, wrap=tk.WORD, height=20)
info_text.pack(side=tk.TOP, padx=(10,10), pady=10, fill=tk.BOTH, expand=True)
info_text.config(padx=10, pady=10)

info_scrollbar = tk.Scrollbar(info_text)
info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
info_text.config(yscrollcommand=info_scrollbar.set)
info_scrollbar.config(command=info_text.yview)

root.mainloop()
