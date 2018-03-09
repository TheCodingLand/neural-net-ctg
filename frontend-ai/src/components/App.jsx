import React, { Component } from 'react';
import Reboot from 'material-ui/Reboot';
import Header from './Header'

import Tina from './Tina'



class App extends Component {
  render() {
    return (
      <div>
        <Reboot />
        <Header />
        <Tina />
      </div>
    );
  }
}


export default App;