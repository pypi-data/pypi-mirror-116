from bs4 import BeautifulSoup
from statics import STOCK_STYLING

class Form(object):
  """
  BlitzForms Form Object.\n\n
  create container with a class name being the form_name supplied.\n
  add class .blitzforms to the container for styling to be applied. style insertion could all together be prevented with passing no_style=True in build method.
  """
  
  def __init__(self, form_name: str, form_handler_endpoint: str, method: str = 'GET'):
    self.form_name = form_name
    self.handler_endpoint = form_handler_endpoint
    self.method = method
    self.fields = []
    
  def add_field(self, type: str, name: str = None, id: str = None, class_: str = None, placeholder: str = None, options: list[str] = None, label: str = None, href: str = None) -> None:
    """
    Method to add a field to the form \n
    type could be any of [text, select, password, submit, button]\n
    --> if type is select, pass in the options as a list of values \n
    placeholder is the literal placeholder for text and password type fields and is the inner content in the case of submit or button\n
    """ 
    self.fields.append({'type': type, 'name': name, 'id': id, 'class': class_, 'placeholder': placeholder, 'options': options, 'label': label, 'href': href})
    
  def build(self, template: str, no_style: bool = False) -> str:
    """
    takes in template, builds the form into the template, and returns updated template.
    no_style will not insert default blitzforms styles if set to True
    """
    soup = BeautifulSoup(template, 'html.parser')

    # building forms
    slots = soup.find_all(class_ = self.form_name)
    for container in slots:
      container.append(self.build_form_from_fields(soup, no_style))
    return str(soup)
      
  def build_form_from_fields(self, template_soup, no_style) -> str:
    """
    internal function to convert self into form markup
    """
    
    # soup onject to call tag creation method
    soup = BeautifulSoup('', 'html.parser') 
    
    # inserting the styling
    if not no_style:
      head = template_soup.find('head')
      styling = STOCK_STYLING
      style = soup.new_tag('style')
      style.append(styling)
      head.append(style)
      
    form = soup.new_tag('form')
    form['action'] = self.handler_endpoint
    form['method'] = self.method

    for field in self.fields:
      placeholder = field['placeholder'] if field['placeholder'] else ''
      class_ = field['class'] if field['class'] else ''
      id = field['id'] if field['id'] else ''
      name = field['name'] if field['name'] else ''
      type = field['type'] 
      
      # adding labels if specified
      if field['label']: 
        label = soup.new_tag('label')
        label.append(field['label']) 
        form.append(label)

      # adding appropriate field
      if type == 'text':
        tag = soup.new_tag('input')
        tag['type'] = 'text'
        tag['placeholder'] = placeholder if placeholder else ''
        tag['class'] = class_ if class_ else ''
        tag['id'] = id if id else ''
        tag['name'] = name if name else ''
      elif type == 'password':
        tag = soup.new_tag('input')
        tag['type'] = 'password'
        tag['placeholder'] = placeholder if placeholder else ''
        tag['class'] = class_ if class_ else ''
        tag['id'] = id if id else ''
        tag['name'] = name if name else ''
      elif type == 'select':
        tag = soup.new_tag('select')
        tag['name'] = name if name else ''
        tag['class'] = class_ if class_ else ''
        tag['id'] = id if id else ''
        for option_ in field['options']:
          option = soup.new_tag('option')
          option['value'] = option_ if option_ else ''
          option.append(option_)
          tag.append(option)
      elif type == 'submit':
        tag = soup.new_tag('button')
        tag['type'] = 'submit'
        tag['class'] = class_ if class_ else ''
        tag['id'] = id if id else ''
        tag['name'] = name if name else ''
        tag.append(placeholder)
      elif type == 'button':
        if field['href']:
          href = field['href']
          tag = soup.new_tag('a')
          tag['href'] = href
          button = soup.new_tag('button')
          button['class'] = class_ if class_ else ''
          button['id'] = id if id else ''
          button.append(placeholder)
          tag.append(button)
        else:
          tag = soup.new_tag('button')
          tag['class'] = class_ if class_ else ''
          tag['id'] = id if id else ''
          tag.append(placeholder)
      form.append(tag) 
    return form