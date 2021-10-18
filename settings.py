save_path = ''
granularity_levels = [['@', '#', 'S', '%', '?', '*', '+', ':', ',', '.', ' '],
                      ['№', '@', '#', 'S', '%', 'a', '?', 'c', '*', '=', '+', ':', ',', '.', '`', ' '],
                      ['№', '@', '#', 'S', '%', 'k', 'a', '?', 'c', 'v', '*', '=', '+', ';',
                       ':', '^', '~', ',', '.', '`', ' '],
                      ['№', '@', '#', 'S', '%', 'U', 'k', 'g', 'h', 'a', '?', 'c', 'v', 't',
                       '*', '=', '+', '!', ';', ':', '^', '~', ',', '.', '`', ' '],
                      ['№', '@', '#', 'S', '%', 'U', 'k', '2', 'g', 'h', 'a', '?', 'c', 'v',
                       '1', 't', '*', '=', '>', '<', '+', '/', '!', ';', ':', '^', '~', ',', '.', '`', ' ']]
text_style = 'font-weight: 500; color: white; font-size: {}pt;'
art_label_style = 'border-style: outset; border-width: 2px; border-color: blue;'
button_style = 'background-color: #570290; border-style: outset; border-width: 2px; border-radius: 10px; ' \
               'border-color: blue; font: bold {}px; min-width: 0em; padding: 6px; color: white;'
size_input_fields_style = 'background : #570290; font-weight: 500; color: white; font-size: {}pt; ' \
                          'border: 2px solid blue; border-picture_width : 2px 2px 2px 2px;'
roberts_filter_checkbox_style = 'background-color: #570290; border-style: outset; border-width: 2px; ' \
                                'border-radius: 0px; border-color: blue; font: bold {}px; min-width: 0em; ' \
                                'padding: 6px; color: white;'
slider_style = """QSlider {} QSlider::groove:horizontal 
{ height: 10px; margin: 0px; border-radius: 5px; background: #B0AEB1; } 
QSlider::handle:horizontal { background: #570290;border: 1px solid #E3DEE2; width: 17px; margin: -5px 0; 
border-radius: 8px; } QSlider::sub-page:qlineargradient { background: #0478C6; border-radius: 5px; } """
