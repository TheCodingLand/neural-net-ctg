
let Api= ((text) =>{
    fetch('http://julien.tech:5005/api/predict',{
        body: JSON.stringify(text),
        method:'POST',
        headers: {
            'content-type': 'application/json'
          },
    } )
.then(result=>result.json())
})

export default Api