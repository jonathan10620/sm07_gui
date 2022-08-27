import PySimpleGUI as sg
from pend_letter_blurb import *
import pyperclip


def open_pend_window(portal):
    sg.theme('DarkAmber')   
    a_items = ['First Name', 'Last Name', 'Medicaid Number', 'Date of Birth',]
    b_items = ['Diagnosis', 'Risk factors', '20 yr. old Dx']
    c_items = ['Requested start date', 'Requested end date', 'Procedure code(s)', 'Applicable modifier', 'MD ordered frequency of clinicial data transmission']
    d_items = ['Physician’s name', 'TPI or NPI', "Physician's signature", 'Missing Date signed']
    e_items = ['Provider printed name','Contact person name', 'Address/City/ZIP', 'Telephone number', 'Fax number', 'TPI', 'NPI', 'Provider’s signature','Date signed']
    other_items = ['Attestation Page Missing','Incorrect Alterations','Invalid Electronic Signature']

    section_A_frame = [
        [sg.Listbox(values=a_items, size=(20,4), enable_events=True, key='A_LIST', select_mode='multiple')],
    ]
    section_B_frame = [
        [sg.Listbox(values=b_items, size=(20,4), enable_events=True, key='B_LIST', select_mode='multiple')],
    ]
    section_C_frame = [
        [sg.Listbox(values=c_items, size=(20,5), enable_events=True, key='C_LIST', select_mode='multiple')],
    ]
    section_D_frame =[
        [sg.Listbox(values=d_items, size=(20,4), enable_events=True, key='D_LIST', select_mode='multiple')],
    ]
    section_E_frame = [
        [sg.Listbox(values=e_items, size=(20,9), enable_events=True, key='E_LIST', select_mode='multiple')],
    ]
    other_frame = [
        [sg.Listbox(values=other_items, size=(20,3), enable_events=True, key='other_LIST', select_mode='multiple')],
    ]

    missing_items_frame = [
        [sg.Frame('Section A',section_A_frame, title_color='white', relief=sg.RELIEF_SUNKEN, key='_FRAME_'),sg.Frame('Section B',section_B_frame, title_color='white', relief=sg.RELIEF_SUNKEN, key='_FRAME_')],
        [sg.Frame('Section C',section_C_frame, title_color='white', relief=sg.RELIEF_SUNKEN, key='_FRAME_'),sg.Frame('Section D',section_D_frame, title_color='white', relief=sg.RELIEF_SUNKEN, key='_FRAME_')],
        [sg.Frame('Section E',section_E_frame, title_color='white', relief=sg.RELIEF_SUNKEN, key='_FRAME_'),sg.Frame('Other',other_frame, title_color='white', relief=sg.RELIEF_SUNKEN, key='_FRAME_')],
    ]
    layout = [
        [sg.Multiline(size=(15, 15), key='textbox'),sg.Frame('Missing Items', missing_items_frame, title_color='white', relief=sg.RELIEF_SUNKEN, font='Any 14') ],
        [sg.Button('Copy'), sg.Button('Close Window')]
    ]  

    # Create the Window
    window = sg.Window('Pend Letter Construction', layout).Finalize()
    #window.Maximize()
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        try:
            item_list = values['A_LIST'] + values['B_LIST'] + values['C_LIST'] + values['D_LIST'] + values['E_LIST'] + values['other_LIST']
        except Exception as e:
            print(e)
            item_list = []
            
        # update multiiline text with listbox selections
        window['textbox'].update('')
        window['textbox'].update('\n'.join(item_list))

        if event == 'Copy':
            leading = 'TMHP is pending your authorization request for the following items:\n'
            text_box = window['textbox'].get()

            
            section_a = ''
            section_b = ''
            section_c = ''
            section_d = ''
            section_e = ''

            body = ''
            

            for item in text_box.split('\n'):
                print(item)
                if item in a_items:
                    # add line one time
                    if 'Section A' not in section_a:
                        section_a += 'Under “Section A: Client information” of the request form, please complete the following:\n'
                    section_a += f'• {item}\n'

                if item in b_items:
                    if 'Section B' not in section_b:
                        section_b += 'Under “Section B: Requested telemonitoring service information” of the request form, please complete the following:\n'
                    if item == 'Diagnosis':
                        section_b += '• Home telemonitoring qualifying diagnosis or condition (must have at least one checked).\n'
                    elif item == 'Risk factors':
                        section_b += '• Risk factors of client (must have at least two checked).\n'
                    elif item == '20 yr. old Dx':
                        section_b += '• For clients 20 years of age and younger,complete one of the home telemonitoring qualifying conditions.\n'
                    
                if item in c_items:
                    if 'Section C' not in section_c:
                        section_c += 'Under “Section C: Authorization period” of the request form, please complete the following:\n'
                    if item == 'Requested start date':
                        section_c += '• Requested start date.\n'
                    elif item == 'Requested end date':
                        section_c += '• Requested end date.\n'
                    elif item == 'Procedure code(s)':
                        section_c += '• Procedure code(s).\n'
                    elif item == 'Applicable modifier':
                        section_c += '• If the initial setup procedure code is requested, enter the procedure code and include the applicable modifier.\n'
                    elif item == 'MD ordered frequency of clinicial data transmission':
                        section_c += '• Physician-ordered frequency of clinical data transmission\n'

                if item in d_items:
                    if 'Section D' not in section_d:
                        section_d += """Under “Section D: Ordering physician information” of the request form, please complete the following:\n"""
                    if item == 'Missing Date signed':
                        section_d += '• Missing Date signed (next to Physician’s signature)\n'
                    else:
                        section_d += f'• {item}\n'

                if item in e_items:
                    if 'Section E' not in section_e:
                        section_e += 'Under “Section E: Telemonitoring provider information” of the request form, please complete the following:\n'
                    if item == 'Date signed':
                        section_e += '• Date signed (next to Physician’s signature)\n'
                    else:
                        section_e += f'• {item}\n'
                # other items        
                if item in other_items:
                    if item == 'Attestation Page Missing':
                        body += attestation_blurb
                    if item == 'Incorrect Alterations':
                        body += alteration_blurb
                    if item == 'Invalid Electronic Signature':
                        body += invalid_electronic_signature_blurb
            if section_c:
                section_c += section_c_trail
            if section_d:
                section_d += section_d_trail
            body += section_a + section_b + section_c + section_d + section_e
            closing = f"""Please use this reference number on your cover sheet when responding via fax or when uploading the required documentation to the PA on the Portal: {portal}
            For your reference, alterations to the original request form must be made with a single line strike-through and additions or corrections must be clearly indicated. All alterations to originals must be initialed and dated. Submissions with whiteout will not be accepted. An electronic alteration is complete when accompanied by initials or signature that have a system—generated date and timestamp, a system-generated logo OR an audit history trail."""
            full_text = leading + body + closing
            pyperclip.copy(full_text)
            
        if event in (None, 'Close Window'):
            # if user closes window or clicks cancel
            break
    window.close()