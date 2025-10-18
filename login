<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login | Disaster Null</title>
  <link rel="stylesheet" href="main.css">
</head>

<body>
  <header>
    <a href="index.html" class="logo">Disaster Null</a>
    <nav>
      <a href="report" >Home</a>
      <a href="report">Report Now</a>
      <a href="volunteer">Find Help</a>
      <a href="saves">Recent Saves</a>
      <a href="about">About</a>
      <a href="login"class="active">Login</a>
    </nav>
  </header>

  <section class="login">
    <h1>Login to Your Account</h1>
    <form action="login_process.php" method="POST">
      <label for="email">Email Address:</label>
      <input type="email" id="email" name="email" required>

      <label for="password">Password:</label>
      <input type="password" id="password" name="password" required>

      <button type="submit" class="btn">Login</button>
      <p>Don’t have an account? <a href="#">Register here</a></p>
    </form>
  </section>

  <footer>
    <p>© 2025 Disaster Null</p>
  </footer>
</body>
</html>
