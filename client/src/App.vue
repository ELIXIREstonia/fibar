<template>
    <div id="app" class="page-container">
      
      <div>
        <b-navbar toggleable="lg" type="dark">
  
          <b-navbar-brand to="/" exact exact-active-class="active" @click="clear">
              FiBar: diameter measuring tool
          </b-navbar-brand>
  
          <b-navbar-nav class="ml-auto">
          <b-nav-item to="/guide" exact exact-active-class="active" right @click="page = 'guide'">User guide</b-nav-item>
          <b-nav-item to="/cite" exact exact-active-class="active" right @click="page = 'about'">Cite FiBar</b-nav-item>
          </b-navbar-nav>
        </b-navbar>
      </div>

      <main>
      <router-view></router-view>
     </main>


      <footer class="footer">
        <hr>
        <p class="copy">
          <a href ="https://elixir.ut.ee/">
            <img src="https://biit.cs.ut.ee/gprofiler/elixir-ee_logo.png" alt="ELIXIR logo" class="elixir-logo">
          </a>
          <a href="https://kogermannlab.com/">
            <img src="./assets/kogermann_lab.png" alt="Kogermann lab logo" class="kogermann-logo" width="300" height="42">
          </a>
        </p>
      <p class="text-muted text-center">
        We respect our users' privacy and therefore we do not store user queries. <br />
        We use cookies to analyze site traffic, including the number of visitors and the pages they visited within the website. <br />
      </p>

    </footer>
      
  
      <!--<p class="copy"> <a style="text-decoration: none !important;" href="https://github.com/marilin99/fibar_tool/tree/main"></a></p>-->
  
    </div>


  </template>
  
  <script>
  
  export default {
    name: 'App',
    data() {
      return {
        page: 'grid',
      }
    },
    methods: {
  clear() {
      window.location.reload();
    }
  }
  }


  </script>
  
  <style lang="scss">
  
  :root {
    --toggle-width: 5rem;
    --toggle-bg-on: coral;
    --toggle-border-on: coral;
  
    --toggle-bg-off: #1F487E;
    --toggle-text-off: #fff;
  }
  
  $theme-colors: ( "primary": #1F487E);
  
  
  @import '~bootstrap/scss/bootstrap.scss';
  @import '~bootstrap-vue/src/index.scss';
  
  .btn.btn-primary {
    color: white;
  }
  
  .btn:active {
    opacity: 0.7;
  }
  
  .float-right {
    float: right;
  }
  
  #app {
    font-family: system-ui, Verdana, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    // display: flex;
    // flex-direction: column;
  }
  
  #app nav {
    background-color: #1F487E;
    margin-bottom: 20px;
  }
  
  #app .navbar-brand img.logo {
    width: 200px;
  }
  
  .version {
    top:9px;
  }
  
  .navbar-brand {
    //background-image: url('assets/logo2.png');
    background-size: auto 100%;
    background-repeat: no-repeat;
    padding-left: 55px;
  }
  
  .navbar-dark .navbar-nav .nav-link {
    //color: white;
  }
  
  // ag-grid
  @import "../node_modules/ag-grid-community/dist/styles/ag-grid.css";
  @import "../node_modules/ag-grid-community/dist/styles/ag-theme-balham.css";
  
  
  
  //.ag-font-style {
  //  user-select: initial;
  //  -moz-user-select: text;
  //  -ms-user-select: text;
  //  -webkit-user-select: text;
  //}
  
  .ag-cell {
    line-height: 18px !important;
    text-align: left;
    //font-size: 12px;
    //padding-left: 8px !important;
    //padding-right: 8px !important;
  }
  
  .ag-cell-focus {
    -webkit-user-select: text;
    -moz-user-select: text;
    -ms-user-select: text;
    user-select: text;
  }
  
  // .footer {
  //   flex-shrink: 0;
  //   margin-top: auto;
  //   width: 100%;
  //   bottom: 0;
  //   position: fixed;

  // }
  // footer
  .reference {
    text-align: left;
    padding-bottom: 15px;
    padding-left: 15px;
    padding-right: 15px;
  }
  
  .copy {
    text-align: center;
    padding-bottom: 15px;
    font-size: 42px;
  }

  .elixir-logo {
    margin-top: 7.5px;
    margin-right: 10px;
    margin-left: 10px;
    height: 70px;
}

  .image {
    margin: 5px;
  }

  .page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

  
  main {
  flex-grow: 1;
}
  
  </style>
  
  