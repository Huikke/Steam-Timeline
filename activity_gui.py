import tkinter as tk
from tkinter import ttk
from activity_fetcher import activity_fetcher

def create_app():
    # 1. Initialize the main window
    root = tk.Tk()
    root.title("Game Activity")

    # 2. Define the data (List of tuples)
    data = activity_fetcher()

    # 3. Create the Treeview widget
    # 'columns' defines the identifier for each column
    columns = ("timestamp", "game", "prev_played_time", "current_played_time", "last_played")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    # 4. Define headings and column widths
    tree.heading("timestamp", text="Timestamp")
    tree.column("timestamp", width=120)
    
    tree.heading("game", text="Game")
    tree.column("game", width=70)
    
    tree.heading("prev_played_time", text="Before")
    tree.column("prev_played_time", width=50)
    
    tree.heading("current_played_time", text="After")
    tree.column("current_played_time", width=50)

    tree.heading("last_played", text="last_played")
    tree.column("last_played", width=120)

    # 5. Insert data into the Treeview
    for item in data:
        tree.insert("", tk.END, values=item)

    # 6. Add a scrollbar for better usability
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    # 7. Layout the widgets
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Start the application
    root.mainloop()

if __name__ == "__main__":
    create_app()