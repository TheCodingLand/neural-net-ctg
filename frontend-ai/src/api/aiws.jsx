
let Api= ((text) =>{
    fetch('http://julien.tech:5005/api/predict',{text:text} )
.then(result=>result.json())
})

export default Api