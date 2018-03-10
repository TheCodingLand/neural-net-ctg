import React, { Component } from 'react';
import Typist from 'react-typist';
import Typography from 'material-ui/Typography';
import { withStyles } from 'material-ui/styles';
import Card, { CardActions, CardContent } from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';
import deepOrange from 'material-ui/colors/deepOrange';
import deepPurple from 'material-ui/colors/deepPurple';

const styles = theme => ({
  chatwindow: {
    position: "relative",
    
},
chatavatar: {
  display:'inline-block',

},
  orangeAvatar: {
    margin: 10,
    color: '#fff',
    backgroundColor: deepOrange[500],
  },
  purpleAvatar: {
    margin: 10,
    color: '#fff',
    
    backgroundColor: deepPurple[500],
  },
  chatsentence: {
    display:'inline-block',
  }
})


class TinaReplies extends Component {


  render() {
    let conversation= this.props.conversation.map((sentense)=> {
    return (<div className={this.props.classes.chatwindow}>
    <div className={this.props.classes.chatavatar}>
    {sentense.user === "Tina" ?  <Avatar className={this.props.classes.purpleAvatar}>{sentense.user.charAt(0)}</Avatar> :<Avatar className={this.props.classes.orangeAvatar}>{sentense.user.charAt(0)}</Avatar>}
    </div>
    <div className={this.props.classes.chatsentence}>
    <Typography classname={this.props.classes.chatsentence} key={sentense.id}>{sentense.content}</Typography></div></div>)
    })

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