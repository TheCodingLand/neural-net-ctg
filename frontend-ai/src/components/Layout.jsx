import React, { Component } from 'react';

import {Grid, Cell} from 'styled-css-grid'
import BrainGraph from './BrainGraph'
import Tina from './Tina'

import Brain from './Brain'
        
       

export default class Layout extends Component {
    render() {
return ( <Grid columns={2} gap="2px">
<Cell height={2}><Tina /> </Cell>
<Cell><Brain /></Cell>
<Cell><BrainGraph /></Cell>
</Grid>
)

    }
}


