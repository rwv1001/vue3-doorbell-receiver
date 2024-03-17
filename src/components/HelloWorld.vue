<template>
  <div class="d-flex">
    <div class="c-item-1 m-0 justify-content-center d-flex">
      <h1 class="align-self-center c-vertical m-0 display-1">Answer</h1>
    </div>
    <div class="c-item-2 m-0 flex-grow-1 d-flex justify-content-center"><h1 class="align-self-center">Answer</h1></div>

  </div>
  <div class="c-topright d-flex">
    <h6 class="p-3">Fr Robert</h6>
    <div class="c-item m-0">
      <nav class="navbar bg-light">
        <div class="container-fluid">

          <button class="navbar-toggler ms-auto" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="list-group">
              <li class="list-group-item active">Cras justo odio</li>
              <li class="list-group-item">Dapibus ac facilisis in</li>
              <li class="list-group-item">Morbi leo risus</li>
              <li class="list-group-item">Porta ac consectetur ac</li>
              <li class="list-group-item">Vestibulum at eros</li>
            </ul>

          </div>
        </div>
      </nav>

    </div>
  </div>

</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
.c-item {
  
  border: 1px solid #333;
  background-color:rgb(176, 190, 136);
  
}

.c-item-1{
  height: 100vh;
  width:190px;
  border: 1px solid #333;
  background-color:rgb(0, 0, 0);
}
.c-item-2{
  height: 100vh;
  width:140px;
  border: 1px solid #333;
  background-color:rgb(255, 255, 255);
}

.c-vertical {
  font-weight: bold;
  color: white;
  transform: rotate(270deg);  
} 

.c-topright {
  position: absolute;
  top: 0px;
  right: 0px;
}

</style>
