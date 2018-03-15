import React, { Component } from 'react';
import Reboot from 'material-ui/Reboot';
import Header from './Header'
import BrainGraph from './BrainGraph'
import Tina from './Tina'
import Layout from './Layout'
import Brain from './Brain'

class App extends Component {
  render() {
    return (
      <div>
        <Reboot />
        <Header />
        <div style= {{position: "relative",
        top:75}} >
        <Layout />
        </div>
       
      </div>
    );
  }
}


export default App;