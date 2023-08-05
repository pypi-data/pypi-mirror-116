STOCK_STYLING = '''
.blitzforms {
  background-color: rgb(241, 241, 241);
}

.blitzforms form {
  display: flex; flex-direction: column; 
}

.blitzforms form * {
  margin-bottom: 5px;
  font-size: 20px;
  font-family: sans-serif;
}

.blitzforms form label {
  margin-top: 7.5px;
}

.blitzforms form label:first-child {
  margin-top: 0px;
}

.blitzforms form button {
  width: fit-content;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 17px;

  border: 1px solid rgb(131, 131, 131);
  border-radius: 5px;

  background-color: rgba(0, 0, 0, 0.03);

  transition: 
    background-color 100ms, 
    transform 300ms cubic-bezier(0.25, 0.1, 0.25, 2.3), 
    padding 300ms cubic-bezier(0.25, 0.1, 0.25, 2.3);
}

.blitzforms form button:hover {
  padding: 10px 22.5px;
  background-color: transparent;
  transform: translateX(-2.5px);
  border-radius: 2px;
}


.blitzforms form *:last-child {
  margin-bottom: 0px;
}

.blitzforms form input, .blitzforms form select {
  padding-left: 5px;
  border: 1px solid rgb(131, 131, 131);
  border-radius: 5px;
}

.blitzforms form input:focus, .blitzforms form select:focus {
  outline: none;
}

.testform {
  width: 300px;
  box-sizing: border-box;
  padding: 15px
}
'''