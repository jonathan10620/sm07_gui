
from helpers import date_check, parse_date, calculate_recieved_date
import PySimpleGUI as sg
import pyperclip
from datetime import datetime, timedelta
from pend_gui import *



sg.theme('Topanga')   




# function that takes two dates and determines difference
client_frame = [
    [sg.Text('Portal ID: ',), sg.InputText(size=(10,20),key='-PORTAL-'),sg.Text('Fax #: '), sg.InputText(size=(12,20))],
    [sg.Text('Age: '), sg.InputText(size=(5),key='-AGE-' )],
    [sg.Text('Procedure: '), sg.Checkbox('S9110'), sg.Checkbox('S9110-U1')],
    [sg.Text('DX: '), sg.Checkbox('Hypertension'), sg.Checkbox('Diabetes')],
    
]

request_date_frame = [
    [sg.Text('Requested DOS: '), sg.InputText(size=(20,20)),sg.Button('Check Date') ],
    [sg.Radio('Approved', 'radio', default=True), sg.Radio('Modified', 'radio'),sg.Radio('Pend', 'radio'), sg.Button('Pend Letters')],
    [sg.Text('Denied DOS: '), sg.InputText(size=(20,20))],
    [sg.Text('Approved DOS: '), sg.InputText(size=(20,20))],
    [sg.Button('Copy'), sg.Button('Clear')],
]

Late_submission_frame = [
    [sg.Button('Provider Blurb'), sg.Button('Client English'),sg.Button('Client Spanish')],
    [sg.Button('HIPPA Blurb')],
]

misc_frame = [
    
]

layout = [
    [
    sg.Frame('Client Info', client_frame, font='Any 12'),sg.Frame('Request Dates', request_date_frame, font='Any 12'),
    sg.Frame('Late Submission Blurbs', Late_submission_frame,font='Any 12'),
    sg.Frame('Miscellaneous', misc_frame, font='Any 12',)
    ]
]

window = sg.Window('Clinician Comment', layout, keep_on_top=False)      

while True:                             # The Event Loop
    event, values = window.read()
    portal, fax, age, tele_ext, set_up, htn_dx, dm_dx, dos, approved, mod, pend, denied_dos,approved_dos = [v for k,v in values.items()]
    # proc set up
    procedure = []
    if tele_ext:
        procedure.append('S9110')
    if set_up:
        procedure.append('S9110-U1')
    
    procedure = ' and '.join(procedure)
    # dx set up
    dx = []
    if htn_dx:
        dx.append('Hypertension')
    if dm_dx:
        dx.append('Diabetes')
    
    dx = ' and '.join(dx)

    try:
        denied_start_string, denied_end_string = denied_dos.split('-')

        denied_start_date = parse_date(denied_end_string)
        # add one day to the date object
        recieved_date = calculate_recieved_date(denied_start_date)
        # convert date object into string
        recieved_date_string = recieved_date.strftime('%m/%d/%Y')
    except ValueError or AttributeError:
        denied_start_string = None
        denied_end_string = None
        recieved_date_string = None
        # sg.popup(f'The date range is not valid, ensure dates seperated by hyphen, ie: 01/01/2020-01/31/2020')

        print('invalid date,ie no hyphen detected')
    if event == 'Copy':        
        if approved:
            try:
                d1, d2 = dos.split('-')
                number_of_days = date_check(d1, d2)
            except:
                number_of_days = -1
                print('Date not correct')
            

            if number_of_days > 180:
                date_start = datetime.strptime(dos.split('-')[0],'%m/%d/%Y')
                print(date_start)
                date_end = date_start + timedelta(days=179)
                print(date_end)
                date_end_string = date_end.strftime('%m/%d/%Y')
                date_start_string = date_start.strftime('%m/%d/%Y')
                approved_dos = f'{date_start_string}-{date_end_string}'
                blurb = f'Portal ID:{portal} Fax #: {fax}. Client is eligible. Duplicates/history checked. None found. Provider is eligible. Provider type: 44. No current or future PDC. Submitter certification page submitted & completed. Requested {procedure} DOS:{dos}. Client age: {age} . The client has a qualifying condition of: {dx} with at least 2 risk factors listed in policy. The dates requested have been modified because the request exceeds the standard authorization period for this service.  DOS {approved_dos} are approved based on Texas Medicaid Medical Policy Manual— October 2022 Telemonitoring Services and SOP 111.J. De La Paz RN.'
                pyperclip.copy(blurb)
                print(blurb)
            elif number_of_days == -1:
                break
            else:
                blurb = f"Portal ID:{portal} Fax #: {fax}. Client is eligible. Duplicates/history checked. None found. Provider is eligible. Provider type: 44. No current or future PDC. Submitter certification page submitted & completed. Requested {procedure} DOS:{dos}. Client age: {age} . The client has a qualifying condition of: {dx} with at least 2 risk factors listed in policy. DOS {dos} are approved based on Texas Medicaid Medical Policy Manual— October 2022 Telemonitoring Services and SOP 111.J. De La Paz RN."
                pyperclip.copy(blurb)
                print(blurb)
        elif mod:
            # create two fields for approved and denied date fields
            d1, d2 = dos.split('-')
            number_of_days = date_check(d1, d2)
            if number_of_days > 180:
                mod_blurb = f"Portal ID:{portal} Fax #: {fax}. Client is eligible. Duplicates/history checked. None found. Provider is eligible. Provider type: 44. No current or future PDC. Submitter certification page submitted & completed. Requested {procedure} DOS:{dos}. Client age: {age} . The client has a qualifying condition of: {dx} with at least 2 risk factors listed in policy. DOS {denied_dos} are denied due to submission guidelines. The dates requested have been modified because the request exceeds the standard authorization period for this service. DOS {approved_dos} are approved based on Texas Medicaid Medical Policy Manual— October 2022 Telemonitoring Services and SOP 111.J. De La Paz RN."
                pyperclip.copy(mod_blurb)
            else:
                mod_blurb = f"Portal ID:{portal} Fax #: {fax}. Client is eligible. Duplicates/history checked. None found. Provider is eligible. Provider type: 44. No current or future PDC. Submitter certification page submitted & completed. Requested {procedure} DOS:{dos}. Client age: {age} . The client has a qualifying condition of: {dx} with at least 2 risk factors listed in policy. DOS {denied_dos} are denied due to submission guidelines. DOS {approved_dos} are approved based on Texas Medicaid Medical Policy Manual— October 2022 Telemonitoring Services and SOP 111.J. De La Paz RN."
                pyperclip.copy(mod_blurb)
        elif pend:
            pend_blurb = f'Portal ID:{portal} Fax #: {fax}. Client is eligible. Duplicates/history checked. None found. Provider is eligible. Provider type: 44. No current or future PDC. Submitter certification page submitted & completed. Requested {procedure} DOS:{dos}. Client age: {age} . The client has a qualifying condition of: {dx} with at least 2 risk factors listed in policy. Based on Texas Medicaid Medical Policy Manual— October 2022 Telemonitoring Services and SOP 111, TMHP is pending your authorization request for the following items: ______ J. De La Paz RN '
            pyperclip.copy(pend_blurb)

        
        

    elif event == 'Provider Blurb':
        late_provider_submission_blurb = f"""The dates of service {denied_start_string}, through {denied_end_string}, were denied because the request was submitted late on {recieved_date_string}.
Providers have three (3) business days from the start of initial telemonitoring services to submit the request. A prior authorization request for subsequent services must be received before the current prior authorization expires. Providers cannot bill clients for services denied because the request was submitted late."""
        
        if number_of_days > 180:
            late_provider_submission_blurb += """\nThe dates requested have been modified because the request exceeds the standard authorization period for this service."""

        pyperclip.copy(late_provider_submission_blurb)
    elif event == 'Client English':
        with open('clinician_blurbs/mod_client_eng.txt', 'r', encoding=('UTF-8')) as f:
            client_blurb = f.read()
            client_english_blurb = client_blurb.replace('___', recieved_date_string)
        pyperclip.copy(client_english_blurb)
        print(client_english_blurb)
        
    elif event == 'Client Spanish':
        with open('clinician_blurbs/mod_client_span.txt','r',encoding=('UTF-8')) as f:
            client_blurb = f.read()
            client_spanish_blurb = client_blurb.replace('___', recieved_date_string)
        pyperclip.copy(client_spanish_blurb)

    elif event == 'HIPPA Blurb':
        if mod:
            hippa_blurb =f"""Portal ID {portal}. HIPAA Verification and Authentication Completed. Modified letters to client/provider sent. J. Delapaz RN"""
            pyperclip.copy(hippa_blurb)
        elif pend:
            hippa_blurb =f"""Portal ID {portal}. HIPAA Verification and Authentication Completed. Pend letter sent to provider. J. Delapaz RN"""
            pyperclip.copy(hippa_blurb)
        else:
            print('HIPPA CLICKED NOTHING COPIED')

    elif event == 'Clear':
        window['-PORTAL-'].update('')
        window['-AGE-'].update('')

    elif event == 'Check Date':
        try:
            d1, d2 = dos.split('-')
            number_of_days = date_check(d1, d2)
            service_units = None
            if number_of_days != 180:
                if number_of_days in range(1,31):
                    service_units = 1
                if number_of_days in range(31,61):
                    service_units = 2
                if number_of_days in range(61,91):
                    service_units = 3
                if number_of_days in range(91,121):
                    service_units = 4
                if number_of_days in range(121,151):
                    service_units = 5
                if number_of_days in range(151,180):
                    service_units = 6
                if number_of_days > 180:
                    service_units = '6 and INFO detail'
                
                sg.popup(f'The date range is {number_of_days} days. This equals {service_units} service units.')
        except Exception as e:
            print(e, '--->DATE ERROR')
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Pend Letters':
        open_pend_window(portal)     

window.close()

