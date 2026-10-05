const http = require('http');
const server = http.createServer((req,res)=>{
    res.write("Live server created suceessfully!!!");
    res.end("\nthis is the end");
})
server.listen(9969);