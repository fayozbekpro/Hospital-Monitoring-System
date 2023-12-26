from flet import *
from config import Database
import sqlite3
from datetime import datetime, timedelta

def admin(page: Page):
	page.title = "Hospital Admin Panel"
	page.theme_mode = "dark"
	page.vertical_alignment = MainAxisAlignment.CENTER
	page.window_width = 700
	page.window_height= 600
	page.window_resizeable = False
	page.scroll = "adaptive"
    # ------- FUNCTIONS
	def change_the_theme_mode(e=0):
		page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
		page.update()
	def OpenSnackBar(val):
		page.snack_bar = SnackBar(Row([Text(val)], alignment=MainAxisAlignment.CENTER))
		page.snack_bar.open = True
		page.update()
	def admin_enterance_function(event):
	    login = enterance_input_login.value
	    password = enterance_input_password.value

	    if len(login) < 2 or len(password) < 2:
	    	OpenSnackBar("Please! Enter login and password.")
	    	return ''
	    else:
	    	db = sqlite3.connect("hospital.db")
	    	cursor = db.cursor()
	    	res = cursor.execute(f"SELECT * FROM admins WHERE login='{login}' AND password='{password}'");
	    	if res.fetchone() == None:
	    		OpenSnackBar("You aren't an admin.")
	    		return ''
	    	else:
	    		main_page.content.clean()
	    		enterance_input_login.value = enterance_input_password.value = ''
	    		main_page.content = admin_panel
	    		app_bar.actions.append(exit_icon_button)
	    		page.client_storage.set("registered", "True")
	    		page.update()
	    	db.commit()
	    	db.close()
	def exit_from_admin(e=''):
		main_page.content = Row([
				Column([enterance_input_login,enterance_input_password,enterance_input_submit], horizontal_alignment=CrossAxisAlignment.CENTER),
			],
			alignment=MainAxisAlignment.CENTER,
			vertical_alignment=CrossAxisAlignment.CENTER,
		)
		app_bar.actions.remove(exit_icon_button)
		page.update()	
		page.client_storage.set("registered", "False")

	def add_patient_get_datetime(e=0):
		nonlocal add_patient_datetime
		add_patient_datetime = add_patient_datetime_picker.value

	def add_patient_get_datetime_dismiss(e=0):
		Alert("Please choose datetime for the patient!")

	def admin_panel_info(e=0):
		with Database() as dbse:
			info_patients = len(dbse.getTableResults("patients"))
			info_all_rooms = len(dbse.getTableResults("rooms"))
			info_available_rooms = len(dbse.getTypeRooms("registered", "'False'"))
			info_occupied_rooms = len(dbse.getTypeRooms("registered", "'True'"))
			info_lux_rooms = len(dbse.getTypeRooms("room_type", "'lux'"))
			info_prelux_rooms = len(dbse.getTypeRooms("room_type", "'prelux'"))
			info_standard_rooms = len(dbse.getTypeRooms("room_type", "'standard'"))

			return Column([
				Row([
					Icon(name=icons.PEOPLE_ROUNDED, color=colors.BLUE, size=20),
					Text(f"Patients: {info_patients}",style=TextThemeStyle.TITLE_SMALL),
					FilledTonalButton(icon=icons.FEATURED_PLAY_LIST_OUTLINED, text="See patients", on_click=show_admin_panel_show_patients),
				]),

				Row([
					Icon(name=icons.BEDROOM_CHILD, color=colors.BLUE, size=20),
					Text(f"All rooms: {info_all_rooms}",style=TextThemeStyle.TITLE_SMALL),
				]),

				Row([
					Icon(name=icons.MEETING_ROOM_SHARP, color=colors.BLUE, size=20),
					Text(f"Available rooms: {info_available_rooms}",style=TextThemeStyle.TITLE_SMALL),
				]),

				Row([
					Icon(name=icons.NO_MEETING_ROOM, color=colors.BLUE, size=20),
					Text(f"Occupied rooms: {info_occupied_rooms}",style=TextThemeStyle.TITLE_SMALL),
				]),

				Row([
					Icon(name=icons.ROOM_SERVICE, color=colors.BLUE, size=20),
					Text(f"Lux rooms: {info_lux_rooms}",style=TextThemeStyle.TITLE_SMALL),
				]),

				Row([
					Icon(name=icons.KING_BED, color=colors.BLUE, size=20),
					Text(f"Pre-Lux rooms: {info_prelux_rooms}",style=TextThemeStyle.TITLE_SMALL),
				]),

				Row([
					Icon(name=icons.SINGLE_BED_OUTLINED, color=colors.BLUE, size=20),
					Text(f"Standard rooms: {info_standard_rooms}",style=TextThemeStyle.TITLE_SMALL),
				]),
			],)

	def show_add_patient_bottom_sheet(e=0):
		admin_panel_add_patient_bottom_sheet.open = True
		admin_panel_add_patient_bottom_sheet.is_scroll_controlled = True
		admin_panel_add_patient_bottom_sheet.update()

	def close_add_patient_bottom_sheet(e=''):
		admin_panel_add_patient_bottom_sheet.open = False
		admin_panel_add_patient_bottom_sheet.update()

	def Alert(text):
			dlg = AlertDialog(
				title=Text(text),
				)
			dlg.open = True
			page.add(dlg)
			page.update()

	def get_patients_floor(e=""):
		if len(add_patient_floor.value) >= 1 and add_patient_floor.value.isnumeric():
			with Database() as dbse:
				res = dbse.getTypeRooms("floor", add_patient_floor.value)
			add_patient_room.options.clear()
			for Data in res:
				add_patient_room.options.append(dropdown.Option(text=f"Room {Data[1]} | Type: {Data[3]}", key=f"{Data[1]} {Data[3]}"))
		else: add_patient_room.options.clear()
		page.update()


	def add_patient_function(e=""):
		nonlocal add_patient_datetime
		if add_patient_name.value == None or add_patient_surname.value == None or add_patient_floor.value == None or add_patient_room.value == None:
			Alert("Please enter all data!")

		elif add_patient_datetime == -1 or len(add_patient_name.value) < 2 or len(add_patient_surname.value) < 2 or len(add_patient_room.value) < 2 or len(add_patient_floor.value) < 1 or len(add_patient_room.value) < 1:
			Alert("Please enter all data!")

		else:
			name,surname, room_num, floor, room_type, registered_date = add_patient_name.value,add_patient_surname.value,add_patient_room.value.split()[0],add_patient_floor.value,add_patient_room.value.split()[1],add_patient_datetime
			with Database() as dbse:
				res = dbse.insertPatient(name,surname, room_num, floor, room_type, registered_date)
				if res >= 1:
					dbse.changeRoomRegistered(room_num, "True")
			if res >= 1:
				Alert("Patient added successfully!")
			else:
				Alert("There was an error. Please try again!") 
			add_patient_room.options.clear()
			add_patient_name.value=add_patient_surname.value=add_patient_room.value=add_patient_floor.value=add_patient_datetime=add_patient_datetime_picker.value=''
			admin_panel = Column([
				admin_panel_info(),
				admin_panel_buttons,
			],)
			main_page.content = admin_panel
			page.update()

	def show_admin_panel_show_patients(e=''):
		admin_panel_show_patients.open = True
		admin_panel_show_patients.update()
		admin_panel_show_patients_list.is_scroll_controlled = True
		with Database() as dbse:
			res = dbse.getTableResults("patients")
			i = 1
			for patient in res:
				admin_panel_show_patients_list.controls.append(Text(f"{i}) {patient[1]} {patient[2]} | Floor: {patient[4]} | Room №{patient[3]}"))
				page.update()
				i+=1


	def get_patients_floor_to_remove(e=""):
		if len(add_patient_floor.value) >= 1 and add_patient_floor.value.isnumeric():
			with Database() as dbse:
				res = dbse.getTypeRooms("floor", add_patient_floor.value)
			add_patient_room.options.clear()
			for Data in res:
				add_patient_room.options.append(dropdown.Option(text=f"Room {Data[1]} | Type: {Data[3]}", key=f"{Data[1]} {Data[3]}"))
		else: add_patient_room.options.clear()
		page.update()

	def close_admin_panel_show_patients(e=''):
		admin_panel_show_patients.open = False
		admin_panel_show_patients.update()
		admin_panel_show_patients_list.controls.clear()
		page.update()

	def show_remove_patient_bottom_sheet(e=0):
		admin_panel_remove_patient_bottom_sheet.open = True
		admin_panel_remove_patient_bottom_sheet.is_scroll_controlled = True
		admin_panel_remove_patient_bottom_sheet.update()

	def close_remove_patient_bottom_sheet(e=''):
		admin_panel_remove_patient_bottom_sheet.open = False
		admin_panel_remove_patient_bottom_sheet.update()


	def get_patients_by_floor(e=""):
		if len(remove_patient_floor.value) >= 1 and remove_patient_floor.value.isnumeric():
			with Database() as dbse:
				res = dbse.executer(f"SELECT * FROM rooms WHERE floor = {remove_patient_floor.value} AND registered = 'True'")
			remove_patient_room.options.clear()
			if len(res) >= 1:
				for Data in res:
					remove_patient_room.options.append(dropdown.Option(text=f"Room {Data[1]} | Type: {Data[3]}", key=f"{Data[1]} {Data[3]}"))
			else:
				remove_patient_selection.options.clear()
				remove_patient_room.options.clear()

		else: remove_patient_room.options.clear()
		page.update()	

	def get_patients_by_room(e=""):
		if len(remove_patient_floor.value) >= 1 and remove_patient_floor.value.isnumeric() and remove_patient_room.value.split(" ")[0] != None and remove_patient_room.value.split(" ")[1] != None :
			with Database() as dbse:
				res = dbse.getTypePatients("floor", remove_patient_floor.value, "room_num", remove_patient_room.value.split(" ")[0])
			remove_patient_selection.options.clear()
			for Data in res:
				remove_patient_selection.options.append(dropdown.Option(text=f"{Data[1]} {Data[2]} | Registered date: {Data[6]}", key=Data[0]))
		else: remove_patient_selection.options.clear()
		page.update()

	def remove_patient_function(e=""):
		if remove_patient_floor.value == None or remove_patient_room.value == None or remove_patient_selection.value == None:
			Alert("Please enter all data!")
		else:
			with Database() as dbse:
				res = dbse.removePatient(remove_patient_selection.value)
			if res >= 1:
				Alert("Patient removed successfully!")
				roomid = remove_patient_room.value.split(" ")[0]
				floorid = remove_patient_floor.value
				with Database() as dbse:
					response = len(dbse.getTypePatients("floor", floorid, "room_num", roomid))
					if response < 1:
						dbse.changeRoomRegistered(roomid, "False")

			else:
				Alert("There was an error. Please try again!") 
			remove_patient_room.options.clear()
			remove_patient_selection.options.clear()
			remove_patient_floor.value=''
			admin_panel = Column([
				admin_panel_info(),
				admin_panel_buttons,
			],)
			main_page.content = admin_panel
			page.update()

    # ------- END FUNCTIONS
	# VARIABLE 
	enterance_input_login = TextField(label="Admin Login", width=350)
	enterance_input_password = TextField(label="Admin Password", width=350)
	enterance_input_submit = OutlinedButton("Move", on_click=admin_enterance_function)
	exit_icon_button = IconButton(icons.EXIT_TO_APP_OUTLINED, on_click=exit_from_admin, style=ButtonStyle(padding=15))
	add_patient_name = TextField(border_color=colors.WHITE,label="Patient's name:", width=350,)
	add_patient_surname = TextField(border_color=colors.WHITE,label="Patient's surname:", width=350)
	add_patient_floor = TextField(border_color=colors.WHITE,label="The floor of the patient:", width=350, on_change=get_patients_floor)
	add_patient_room = Dropdown(border_color=colors.WHITE,width=350, options=[dropdown.Option(text="Please enter the floor number!", )])
	add_patient_datetime_picker = DatePicker(
        on_change=add_patient_get_datetime,
        on_dismiss=add_patient_get_datetime_dismiss,
        first_date=datetime.now(),
        last_date=datetime.now() + timedelta(days=7),)
	page.overlay.append(add_patient_datetime_picker)
	add_patient_datetime = -1

	admin_panel_show_patients_list = ListView(expand=True, spacing=10)



	remove_patient_floor = TextField(border_color=colors.WHITE,label="The floor of the patient:", width=350, on_change=get_patients_by_floor)
	remove_patient_room = Dropdown(border_color=colors.WHITE,width=350, options=[dropdown.Option(text="Please enter the floor number!", )], on_change=get_patients_by_room)
	remove_patient_selection = Dropdown(border_color=colors.WHITE,width=350, options=[dropdown.Option(text="Please enter the floor number and select the room!", )])
# VARIABLE END

# MAIN VARIBLES
	admin_panel_buttons = ResponsiveRow(
            [
                Container(
                    OutlinedButton("Add Patient", style=ButtonStyle(color=colors.BLUE),on_click=show_add_patient_bottom_sheet),
                    padding=5,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),
                Container(
                    OutlinedButton("Remove Patient", style=ButtonStyle(color=colors.BLUE),on_click=show_remove_patient_bottom_sheet),
                    padding=5,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),
                # Container(
                #     ElevatedButton("Add Admin", style=ButtonStyle(color=colors.BLUE),),
                #     padding=5,
                #     col={"sm": 6, "md": 4, "xl": 2},
                # ),
                # Container(
                #     ElevatedButton("Remove Admin", style=ButtonStyle(color=colors.BLUE),),
                #     padding=5,
                #     col={"sm": 6, "md": 4, "xl": 2},)
            ],)
	


	
	admin_enterance = Row([
			Column([enterance_input_login,enterance_input_password,enterance_input_submit], horizontal_alignment=CrossAxisAlignment.CENTER),
		],
		alignment=MainAxisAlignment.CENTER,
		vertical_alignment=CrossAxisAlignment.CENTER,
	)



	admin_panel = Column([
			admin_panel_info(),
			admin_panel_buttons,
		],)

	admin_panel_add_patient_bottom_sheet = BottomSheet(
		Container(Column(
			[
				Column([
					IconButton(icons.CLOSE_SHARP,icon_color=colors.WHITE, on_click=close_add_patient_bottom_sheet),
					add_patient_name,
					add_patient_surname,
					add_patient_floor,
					add_patient_room,
					ElevatedButton(
				        "Pick date",
				        icon=icons.CALENDAR_MONTH,
				        on_click=lambda _: add_patient_datetime_picker.pick_date(),
				    ),
					OutlinedButton("Submit", style=ButtonStyle(color=colors.WHITE,), width=350, on_click=add_patient_function, height=30)
				], horizontal_alignment=CrossAxisAlignment.CENTER, ),
			], horizontal_alignment=CrossAxisAlignment.CENTER,
        	scroll=ScrollMode.ALWAYS,
		), padding=12), bgcolor=colors.BLACK
	)

	admin_panel_remove_patient_bottom_sheet = BottomSheet(
		Container(Column(
			[
				Column([
					IconButton(icons.CLOSE_SHARP,icon_color=colors.WHITE, on_click=close_remove_patient_bottom_sheet),
					remove_patient_floor,
					remove_patient_room,
					remove_patient_selection,
					OutlinedButton("Submit", style=ButtonStyle(color=colors.WHITE,), width=350, on_click=remove_patient_function, height=30)
				], horizontal_alignment=CrossAxisAlignment.CENTER, ),
			], horizontal_alignment=CrossAxisAlignment.CENTER,
        	scroll=ScrollMode.ALWAYS,
		), padding=12), bgcolor=colors.BLACK
	)


	admin_panel_show_patients = BottomSheet(
		Container(Column([
			IconButton(icons.CLOSE_SHARP,icon_color=colors.WHITE, on_click=close_admin_panel_show_patients),
			Row([
				admin_panel_show_patients_list
			], )
		],scroll=ScrollMode.ALWAYS), padding=30)
	)

	# END MAIN VARIBLES

	main_page = Container(content=admin_enterance)


	app_bar = AppBar(
			title=Text("Admin Panel"),
			actions=[
				IconButton(icons.SUNNY, on_click=change_the_theme_mode, style=ButtonStyle(padding=15),),
			],
		)
	if page.client_storage.get("registered") == None or page.client_storage.get("registered") != "True":
		main_page.content = admin_enterance
		page.update()
	else:
		main_page.content = admin_panel
		app_bar.actions.append(exit_icon_button)
		page.update()

	page.add(admin_panel_show_patients)
	page.add(admin_panel_add_patient_bottom_sheet)
	page.add(admin_panel_remove_patient_bottom_sheet)
	page.add(main_page)
	page.add(app_bar)
	page.update()

app(target=admin)