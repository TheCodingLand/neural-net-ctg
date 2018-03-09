import React, { Component } from 'react';
import TextField from 'material-ui/TextField';
import Typist from 'react-typist';
import Typography from 'material-ui/Typography';
import { withStyles } from 'material-ui/styles';
import Card, { CardActions, CardContent } from 'material-ui/Card';

const styles = theme => ({
  chatwindow: {
  },
})


class TinaReplies extends Component {


  render() {
    let conversation= this.props.conversation.map((sentense)=> {
    return <Typography key={sentense.id}> {sentense.user} : {sentense.content}</Typography>})

    return (
      <div classname={this.props.classes.chatwindow}>
        <Card>
          {conversation}
        </Card>
        
      
      </div>
    );
  }
}


export default withStyles(styles)(TinaReplies)