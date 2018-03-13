import React, { Component } from 'react';
import Reboot from 'material-ui/Reboot';
import Header from './Header'
import BrainGraph from './BrainGraph'
import Tina from './Tina'

import Brain from './Brain'

class App extends Component {
  render() {
    return (
      <div>
        <Reboot />
        <Header />
        <Tina />
        <Brain />
        <BrainGraph />
      </div>
    );
  }
}


export default App;