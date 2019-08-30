<?php

$data = run();

function run()
{
    checkMethod('GET');

    try {
        $_data = $_GET;
    } catch (Exception $e) {
        http_response_code(400);
        die();
    }

    return $_data;
}

function checkMethod($method)
{
    if ($_SERVER['REQUEST_METHOD'] != $method) {
        http_response_code(405);
        die('Method not allowed');
    }
}

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Basic -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">   
   
    <!-- Mobile Metas -->
    <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
 
     <!-- Site Metas -->
    <title>GoodWEB Solutions - Responsive HTML5 Landing Page Template</title>  
    <meta name="keywords" content="">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Site Icons -->
    <link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon" />
    <link rel="apple-touch-icon" href="images/apple-touch-icon.png">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <!-- Site CSS -->
    <link rel="stylesheet" href="style.css">
    <!-- Responsive CSS -->
    <link rel="stylesheet" href="css/responsive.css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="css/custom.css">
    <!-- Spinner CSS -->
    <link type="text/css" rel="stylesheet" href="../spinner/waitMe.css">

    <!-- Modernizer for Portfolio -->
    <script src="js/modernizer.js"></script>

    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>
<!-- LOADER -->
<div id="preloader">
        <div class="loader">
			<div class="loader__bar"></div>
			<div class="loader__bar"></div>
			<div class="loader__bar"></div>
			<div class="loader__bar"></div>
			<div class="loader__bar"></div>
			<div class="loader__ball"></div>
		</div>
    </div><!-- end loader -->
    <!-- END LOADER -->
    
	<div class="top-bar">
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-6 col-sm-6">
					<div class="left-top">
						<div class="email-box">
							<a href="#"><i class="fa fa-envelope-o" aria-hidden="true"></i> youremail@gmail.com</a>
						</div>
						<div class="phone-box">
							<a href="tel:1234567890"><i class="fa fa-phone" aria-hidden="true"></i> +1 234 567 890</a>
						</div>
					</div>
				</div>
				<div class="col-md-6 col-sm-6">
					<div class="right-top">
						<div class="social-box">
							<ul>
								<li><a href="#"><i class="fa fa-facebook-square" aria-hidden="true"></i></a></li>
								<li><a href="#"><i class="fa fa-instagram" aria-hidden="true"></i></a></li>
								<li><a href="#"><i class="fa fa-linkedin-square" aria-hidden="true"></i></a></li>
								<li><a href="#"><i class="fa fa-twitter-square" aria-hidden="true"></i></a></li>
								<li><a href="#"><i class="fa fa-rss-square" aria-hidden="true"></i></a></li>
							<ul>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
    <header class="header header_style_01">
        <nav class="megamenu navbar navbar-default">
            <div class="container-fluid">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="index.html"><img src="images/logos/logo.png" alt="image"></a>
                </div>
                <div id="navbar" class="navbar-collapse collapse">
                    <ul class="nav navbar-nav navbar-right">
                        <li><a href="index.html">Home</a></li>
                        <li><a href="about-us.html">About us</a></li>
                        <li><a href="services.html">Our Services</a></li>
                        <li><a href="features.html">Features</a></li>
                        <li><a class="active" href="applyjob.html">Apply</a></li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>

   	<div class="banner-area banner-bg-1">
		<div class="container">
			<div class="row">
				<div class="col-md-12">
                <div class="banner">
						<h2>Apply for a Job</h2>
						<ul class="page-title-link">
							<li><a href="#">Home</a></li>
							<li><a href="#">Apply</a></li>
						</ul>
					</div>
				</div>
			</div>
		</div>
    </div>
    
    <div id="about" class="section wb">
        <div class="container">
            <div class="section-title text-center">
                <h3>Apply for a job in our company</h3>
                <p class="lead">You have successfully logged in via VidChain. <br>Please submit your information to apply for the job.<br>We are delighted about your interest of working with us!</p>
            </div><!-- end title -->
            <div class="row">
				<div class="col-md-6">
                    <div class="post-media wow fadeIn">
                        <!-- USER VidChain Full Image Start -->
                        <div class="student_full_image">
                            <?php
                            if (isset($data['photo'])){
                                echo '<img src="'.$data['photo'].'" alt="user profile" class="img-responsive img-rounded">';
                            }else{
                                echo'<img src="uploads/about_02.jpg" alt="" class="img-responsive img-rounded">';
                            }
                            ?>
                        </div>
                    </div><!-- end media -->
                </div><!-- end col -->
				
                <div class="col-md-6 col-12">
                    <!-- User Details Info Area Start -->
                    <div class="teacher_details_info">
                        <!-- User Name Designation Start -->
                        <div class="name_designation">
                            <h2><?php echo $data['name'];?></h2>
                            <?php
                            if (isset($data['nif'])){
                                echo '<h5>'.$data['nif'].'</h5>';
                            }
                            ?>
                            
                        </div>
                        <div class="teacher_contact_info">
                            <!-- Single Contact Info Start -->
                            <div class="tea_single_contact_info">
                                <div class="contact_icon">
                                    <i class="fa fa-envelope-o" aria-hidden="true"></i>
                                </div>
                                <div class="contact_data">
                                    <p><?php echo $data['email'];?></p>
                                </div>
                            </div>
                            <!-- Single Contact Info Start -->
                            <div class="tea_single_contact_info">
                                <div class="contact_icon">
                                    <i class="fa fa-mobile" aria-hidden="true"></i>
                                </div>
                                <div class="contact_data">
                                    <p><?php echo $data['phone'];?></p>
                                </div>
                            </div>
                            <!-- Single Contact Info Start -->
                            <div class="tea_single_contact_info">
                                <div class="contact_icon">
                                    <i class="fa fa-graduation-cap" aria-hidden="true"></i>
                                </div>
                                <div class="contact_data">
                                    <p><?php echo $data['education'];?></p>
                                </div>
                            </div>
                        </div>  <!-- User Contact Info End -->
                    </div> <!-- Teacher Details Info Area End -->
                </div><!-- end col -->   
            </div><!-- end row -->
            <div class="row">
                <hr class="hr2"> 
                <div class="contact_form demo-vidchain demo_form">
                    <div class="col-md-12">
                        <button type="button" id="demo" class="btn btn-light btn-radius btn-brd grd1 btn-block show-btn">Apply for the job</button>
                        <div id="job" class="job-accepted"><h4>You got the job! CONGRATULATIONS!</h4></div> 
                        <div class="contact_data job-accepted">
                            <button class="btn btn-default sign_in_vidchain btn-sm" id="validate-elicence" onclick="validateElicence(3, 'Product Designer', '<?php echo $data['token'];?>')"><img src="./img/vidchain-ico.png" style="margin-right: 10px;" /> <strong>INCLUDE IN MY VIDCHAIN WALLET</strong><span class="glyphicon glyphicon-refresh spinning" style="margin-left: 10px;"></span></button>
                        </div>
                    </div> 
                </div>  
            </div>
        </div><!-- end container -->
    </div><!-- end section -->

    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-4 col-sm-4 col-xs-12">
                    <div class="widget clearfix">
                        <div class="widget-title">
                            <img src="images/logos/logo-2.png" alt="" />
                        </div>
                        <p> Integer rutrum ligula eu dignissim laoreet. Pellentesque venenatis nibh sed tellus faucibus bibendum. Sed fermentum est vitae rhoncus molestie. Cum sociis natoque penatibus et magnis dis montes.</p>
                        <p>Sed fermentum est vitae rhoncus molestie. Cum sociis natoque penatibus et magnis dis montes.</p>
                    </div><!-- end clearfix -->
                </div><!-- end col -->

				<div class="col-md-4 col-sm-4 col-xs-12">
                    <div class="widget clearfix">
                        <div class="widget-title">
                            <h3>Pages</h3>
                        </div>

                        <ul class="footer-links hov">
                            <li><a href="#">Home <span class="icon icon-arrow-right2"></span></a></li>
							<li><a href="#">Blog <span class="icon icon-arrow-right2"></span></a></li>
							<li><a href="#">Pricing <span class="icon icon-arrow-right2"></span></a></li>
							<li><a href="#">About <span class="icon icon-arrow-right2"></span></a></li>
							<li><a href="#">Faq <span class="icon icon-arrow-right2"></span></a></li>
							<li><a href="#">Contact <span class="icon icon-arrow-right2"></span></a></li>
                        </ul><!-- end links -->
                    </div><!-- end clearfix -->
                </div><!-- end col -->
				
                <div class="col-md-4 col-sm-4 col-xs-12">
                    <div class="footer-distributed widget clearfix">
                        <div class="widget-title">
                            <h3>Subscribe</h3>
							<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which one know this tricks.</p>
                        </div>
						
						<div class="footer-right">
							<form method="get" action="#">
								<input placeholder="Subscribe our newsletter.." name="search">
								<i class="fa fa-envelope-o"></i>
							</form>
						</div>                        
                    </div><!-- end clearfix -->
                </div><!-- end col -->
            </div><!-- end row -->
        </div><!-- end container -->
    </footer><!-- end footer -->

    <div class="copyrights">
        <div class="container">
            <div class="footer-distributed">
                <div class="footer-left">                   
                    <p class="footer-company-name">All Rights Reserved. &copy; 2018 <a href="#">GoodWEB</a> Design By : 
					<a href="https://html.design/">html design</a></p>
                </div>

                
            </div>
        </div><!-- end container -->
    </div><!-- end copyrights -->

    <a href="#" id="scroll-to-top" class="dmtop global-radius"><i class="fa fa-angle-up"></i></a>


    <!-- ===================== All jQuery Plugins ===================== -->

    <!-- ALL JS FILES -->
    <script src="js/all.js"></script>
    <!-- ALL PLUGINS -->
    <script src="js/custom.js"></script>
    <script src="js/portfolio.js"></script>
    <script src="js/hoverdir.js"></script>    

    <!-- Tether js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
    <script src="//rawgit.com/saribe/eModal/master/dist/eModal.min.js"></script>
    <script src="../assets/js/fake-login-success.js"></script>
    <script src="../assets/js/job-offer.js"></script>
    <script src="../spinner/waitMe.js"></script>

    <!-- ViDChain Modal -->
    <div class="modal fade" id="validateModal" role="dialog" aria-hidden="true">
        <div class="vertical-alignment-helper">
            <div class="modal-dialog vertical-align-center">
                <div class="modal-content">
                    <!-- Modal Header -->
                    <div class="modal-header">
                        <h3 class="modal-title" id="modal-title">
                            Validating attributes ...
                        </h3>
                    </div>
                    
                    <!-- Modal Body -->
                    <div id="modal-body" class="modal-body">                                 
                       <p>Please, check your ViDChain APP in order to include your attribute in your ViDChain Wallet</p>                                                   
                    </div>
                    
                    <!-- Modal Footer -->
                    <div class="modal-footer">
                        <div id="btnValidate">
                            <button type="button" class="btn btn-default" id="btnclose" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- /Add Service Modal -->

</body>

</html>