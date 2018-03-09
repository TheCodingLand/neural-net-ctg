import 'core-js/fn/array/includes';
import 'core-js/es6/set';
//import 'core-js/fn/array/map';
import 'core-js/es6/map';
import 'raf/polyfill';

import React from 'react';
import ReactDOM from 'react-dom';

import App from './components/App';
import registerServiceWorker from './registerServiceWorker';
import { BrowserRouter } from 'react-router-dom'
import Reboot from 'material-ui/Reboot';
import { teal, red } from 'material-ui/colors';
import 'typeface-roboto'
import { MuiThemeProvider, createMuiTheme } from 'material-ui/styles';
import amber from 'material-ui/colors/amber';
import indigo from 'material-ui/colors/indigo';
import store from './Store'
import { Provider } from "react-redux"


const theme = createMuiTheme({
  typography: {
    fontWeightLight: 200,
    fontWeightRegular: 300,
    fontWeightMedium: 500
  },
  palette: {

    type: 'light', 
    primary: {
        ...teal,
        A700: '#009b7b',
      },
    
      
}
}
);


ReactDOM.render(<Provider store={store}><MuiThemeProvider theme={theme}>
  <BrowserRouter><App /></BrowserRouter> </MuiThemeProvider></Provider>, document.getElementById('root'));
registerServiceWorker();
