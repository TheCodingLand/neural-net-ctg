import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Button from 'material-ui/Button';
import IconButton from 'material-ui/IconButton';
import MenuIcon from 'material-ui-icons/Menu';




const styles = theme => ({
    root: {
        flexGrow: 1,
    },
    flex: {
        flex: 1,
    },
    menuButton: {
        marginLeft: -12,
        marginRight: 20,
    },
  
});

let browserHandler = {
    
    default: (browser) => {return <img height='64px' src={'images/browsers/'+browser+'/'+browser+'.png'} /> } ,
    
  }

class Header extends React.Component {


    render() {

        const { classes } = this.props;
        return <div style={{}}>
            <AppBar position="fixed">
                <Toolbar>
                    <IconButton className={classes.menuButton} color="inherit" aria-label="Menu">
                        <MenuIcon />
                    </IconButton>
                    
                    <Typography variant="title" color="inherit" style={{ padding: '0.5em' }} className={classes.flex}>
                        CTG TINA AI
                    </Typography>
                  
                 {/* <Button className="loginButton" color="inherit">Login</Button> */}
                 <Button className="loginButton" color="inherit" href="https://github.com/TheCodingLand/neural-net-ctg">
               Source Code on GitHub
                </Button>
                </Toolbar>

            </AppBar>



        </div >
    }
}




export default withStyles(styles)(Header)