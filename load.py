import Tkinter as tk
import ttk

import math

settings_open = False

class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(1)
        self.text = text

        self.title_frame = tk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        self.toggle_button = tk.Label(self.title_frame,text= unichr(9654) + ' ' + text)
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self)

        def toggle(self):
            if bool(self.show.get()):
                self.sub_frame.pack(fill="x", expand=1)
                self.toggle_button.configure(text=unichr(9660) + ' ' + self.text)
                self.show.set(0)
            else:
                self.sub_frame.forget()
                self.toggle_button.configure(text= unichr(9654) + ' ' + self.text)
                self.show.set(1)

        def click(event):
          toggle(self)

        self.toggle_button.bind("<Button-1>",click)

class Dialog(tk.Toplevel):

    def __init__(self, parent, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180 to + 180 which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def plugin_start():
    """
    Load this plugin into EDMC
    """
    print "bearing started"
    return "za bearing"

def plugin_app(parent):
    """
    Create a TK widget for the EDMC main window
    """
    plugin_app.frame = tk.Frame(parent)
    plugin_app.lbl_frm = tk.Frame(plugin_app.frame)
    plugin_app.lbl = tk.Label(plugin_app.lbl_frm, text="Bearing:", anchor=tk.W)
    plugin_app.target_lat = tk.Entry(plugin_app.frame, width=1)
    plugin_app.lat_label = tk.Label(plugin_app.frame, text='Lat:')
    plugin_app.target_lon = tk.Entry(plugin_app.frame, width=1)
    plugin_app.lon_label = tk.Label(plugin_app.frame, text='Lon:')
    plugin_app.bearing_frame = tk.Frame(plugin_app.lbl_frm)
    plugin_app.set_btn = tk.Button(plugin_app.lbl_frm, text='Set', command = toggle_settings)
    plugin_app.lbl_left = tk.Label(plugin_app.bearing_frame, text='<', width=1)
    plugin_app.lbl_right = tk.Label(plugin_app.bearing_frame, text='>', width=1)
    plugin_app.bearing = tk.Label(plugin_app.bearing_frame, text='', width=6)
    plugin_app.lbl_frm.grid(row=0,column=0, columnspan=4, sticky='nsew')
    plugin_app.lbl_frm.grid_columnconfigure(0, weight=1, uniform="fred")
    plugin_app.lbl_frm.grid_columnconfigure(1, weight=1, uniform="fred")
    plugin_app.lbl_frm.grid_columnconfigure(2, weight=1, uniform="fred")
    plugin_app.frame.grid_columnconfigure(1, weight=1)
    plugin_app.frame.grid_columnconfigure(3, weight=1)
    plugin_app.lbl.grid(sticky=tk.W)
#    plugin_app.lat_label.grid(row=1, column=0)
#    plugin_app.target_lat.grid(row=1, column=1, sticky = "nsew")
#    plugin_app.lon_label.grid(row=1, column=2)
#    plugin_app.target_lon.grid(row=1, column=3, sticky = "nsew")
    plugin_app.bearing_frame.grid(row=0, column=1, sticky = "nsew")
    plugin_app.lbl_left.grid(row=0, column=0)
    plugin_app.bearing.grid(row=0, column=1)
    plugin_app.lbl_right.grid(row=0, column=2)
    plugin_app.set_btn.grid(row=0, column=2, sticky="e")
    print "bearing loaded"
    return (plugin_app.frame)

def toggle_settings():
    global settings_open
    if settings_open == False:
        plugin_app.lat_label.grid(row=1, column=0)
        plugin_app.target_lat.grid(row=1, column=1, sticky = "nsew")
        plugin_app.lon_label.grid(row=1, column=2)
        plugin_app.target_lon.grid(row=1, column=3, sticky = "nsew")
        plugin_app.set_btn.config(text='OK')
        settings_open = True
    else:
        plugin_app.lat_label.grid_forget()
        plugin_app.target_lat.grid_forget()
        plugin_app.lon_label.grid_forget()
        plugin_app.target_lon.grid_forget()
        plugin_app.set_btn.config(text='Set')
        settings_open = False

def scrub_journal_entry(cmdr, system, station, entry, state):
    global settings_open
    if entry['event'] == 'Location':
        if 'Latitude' in entry:
            plugin_app.lbl_frm.grid(row=0,column=0, columnspan=4, sticky='nsew')
        else:
            settings_open = True
            toggle_settings()
            plugin_app.lbl_frm.grid_forget()
    elif entry['event'] == 'ApproachBody':
        plugin_app.lbl_frm.grid(row=0,column=0, columnspan=4, sticky='nsew')
    elif entry['event'] in ['LeaveBody','FSDJump']:
        settings_open = True
        toggle_settings()
        plugin_app.lbl_frm.grid_forget()

def dashboard_entry(cmdr, is_beta, entry):
    if "Latitude" in entry:
        try:
            current_lat_lon = (entry["Latitude"], entry["Longitude"])
            target_lat_lon = (float(plugin_app.target_lat.get()), float(plugin_app.target_lon.get()))
            bearing = calculate_initial_compass_bearing(current_lat_lon, target_lat_lon)
            txt_bearing = "%.2f" % bearing
            correction = (360 + (bearing - entry['Heading'])) % 360
            plugin_app.bearing.config(text=txt_bearing)
            if 1 < correction < 180:
                plugin_app.lbl_right.config(text=">")
            else:
                plugin_app.lbl_right.config(text="")
            if 180 < correction < 359:
                plugin_app.lbl_left.config(text="<")
            else:
                plugin_app.lbl_left.config(text="")
        except:
            plugin_app.bearing.config(text="!")
            plugin_app.lbl_left.config(text="<")
            plugin_app.lbl_right.config(text=">")
    else:
        plugin_app.bearing.config(text="")
        plugin_app.lbl_left.config(text="<")
        plugin_app.lbl_right.config(text=">")