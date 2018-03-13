

import React, { Component } from 'react';

import { connect } from "react-redux"
import {Doughnut} from 'react-chartjs-2';
function mapStateToProps(state) {
    return {
        user: state.user
    }

}


class BrainGraph extends Component {

    getData = () => {
        let labels = ['none']
        let data =[0]
        let total = 0
        if (this.props.user.brain) { labels = this.props.user.brain.map((neuron) => {return neuron.category})
        this.props.user.brain.forEach(element => { total = total + element.confidence
            
        });
       
        console.log('total' + total)
        data= this.props.user.brain.map((neuron) => {return neuron.confidence*100/total})
    }
        console.log(data)
        return {
            labels: labels,
               
            datasets: [{
              data: data,
              backgroundColor: [
              '#29CFAA',
              '#36FF84',
              '#DD22FF',
              '#FFCE56',
              '#36A2EB',
              
              
              ],
              hoverBackgroundColor: [
              '#FF6384',
              '#36A2EB',
              '#36FF84',
              '#DD22FF',
              '#FFCE56'
              ]
            }]
          }
          }
        
    render() {
    
       
      return (
        <div style={{padding : '100px', width : '600px', height:"600px"}}><Doughnut data={this.getData.bind(this)} />
            </div>
      )}
  }

export default connect(mapStateToProps)(BrainGraph)