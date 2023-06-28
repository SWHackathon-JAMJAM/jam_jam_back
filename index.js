let express=require('express');
let app=express();
let path=require('path');
const cors=require('cors');
app.use(cors());

app.use(express.static(path.join(__dirname)));

app.get('/',function(res,req){
    res.sendFile(path.join(__dirname,'index.html'));
})


app.listen(8081,function(){
    console.log("Server start");
})
