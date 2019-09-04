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
    <meta charset="UTF-8">
    <meta name="description" content="">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <!-- Title  -->
    <title>Sample University</title>

    <!-- Favicon  -->
    <link rel="shortcut icon" href="img/core-img/favicon.ico">

    <!-- ===================== All CSS Files ===================== -->

    <!-- Style css -->
    <link rel="stylesheet" href="style.css">

    <!-- Responsive css -->
    <link rel="stylesheet" href="css/responsive.css">

    <!-- Color Changer css -->
    <link rel="stylesheet" href="css/color-changer.css">

    <!--[if IE]>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/respond.js/1.4.2/respond.min.js"></script>
	<![endif]-->

</head>

<body>
    <!-- Color Changer Area Start -->
    <div class="color_palate" id="color_changer">
        <div class="single_color" id="color_1"></div>
        <div class="single_color" id="color_2"></div>
        <div class="single_color" id="color_3"></div>
        <div class="single_color" id="color_4"></div>
    </div>

    <!-- preloader start -->
    <div id="preloader"></div>
    <!-- /.end preloader -->
    
    <!--  ===================== Header Area Start ===================== -->
    <header class="header_area">
        <!-- Top Header Area Start -->
        <div class="top_header_area hidden-xs">
            <div class="container">
                <div class="row">
                    <div class="col-md-3 col-lg-5">
                        <!--  Top Quote Area Start -->
                        <div class="top_quote hidden-sm">
                            <p>Welcome to Sample University.</p>
                        </div>
                    </div>
                    <div class="col-md-9 col-lg-7">
                        <div class="social_reg_log_area">
                            <!--  Top Social bar start -->
                            <div class="top_social_bar">
                                <a href="#"><i class="fa fa-facebook" aria-hidden="true"></i></a>
                                <a href="#"><i class="fa fa-twitter" aria-hidden="true"></i></a>
                                <a href="#"><i class="fa fa-linkedin" aria-hidden="true"></i></a>
                                <a href="#"><i class="fa fa-skype" aria-hidden="true"></i></a>
                                <a href="#"><i class="fa fa-dribbble" aria-hidden="true"></i></a>
                            </div>
                            <!--  Login Register Area -->
                            <div class="login_register">

                                <div class="reg">
                                    <i class="fa fa-user" aria-hidden="true"></i>
                                    <a href="student-detail.html">Profile</a>
                                </div>
                            </div>

                            <div class="language_area">
                                <div class="dropdown">
                                    <button aria-expanded="false" aria-haspopup="true" data-toggle="dropdown" id="lag" type="button" class="btn btn-default dropdown-toggle">
                                        <i class="fa fa-globe" aria-hidden="true"></i>Language
                                        <i class="fa fa-caret-down" aria-hidden="true"></i>
                                    </button>
                                    <ul aria-labelledby="lag" class="dropdown-menu">
                                        <li>
                                            <a href="#"><img alt="" src="img/core-img/lan-1.jpg">English</a>
                                        </li>
                                        <li>
                                            <a href="#"><img alt="" src="img/core-img/lan-2.jpg">German</a>
                                        </li>
                                        <li>
                                            <a href="#"><img alt="" src="img/core-img/lan-3.jpg">Spanish</a>
                                        </li>
                                        <li>
                                            <a href="#"><img alt="" src="img/core-img/lan-4.jpg">Bangla</a>
                                        </li>
                                        <li>
                                            <a href="#"><img alt="" src="img/core-img/lan-5.jpg">China</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Top Header Area  End -->

        <!-- Main Header Area Start -->
        <div class="main_header_area home2">
            <div class="container">
                <div class="row">
                    <div class="col-md-3 col-12">
                        <!-- Logo Area -->
                        <div class="logo_area">
                            <a href="index.html"><img src="img/core-img/logo.png" alt=""></a>
                        </div>
                    </div>

                    <div class="col-md-9 col-12">
                        <!-- Menu Area -->
                        <div class="main_menu_area">
                            <div class="mainmenu">
                                <nav>
                                    <ul id="nav">
                                        <li class="current_page_item"><a href="#">Home<i class="fa fa-caret-down" aria-hidden="true"></i></a>
                                            <ul class="sub-menu">
                                                <li><a href="index.html">Home-1</a></li>
                                                <li><a href="index-two.html">Home-2</a></li>
                                            </ul>
                                        </li>
                                        <li><a href="#">pages<i class="fa fa-caret-down" aria-hidden="true"></i></a>
                                            <ul class="sub-menu">
                                                <li><a href="#">Home Pages<i class="fa fa-caret-right" aria-hidden="true"></i></a>
                                                    <ul class="sub-menu">
                                                        <li><a href="index.html">Home-1</a></li>
                                                        <li><a href="index-two.html">Home-2</a></li>
                                                    </ul>
                                                </li>
                                                <li><a href="#">Other Pages<i class="fa fa-caret-right" aria-hidden="true"></i></a>
                                                    <ul class="sub-menu">
                                                        <li><a href="about-us.html">About Us</a></li>
                                                        <li><a href="code-of-contact.html">Code of Contact</a></li>
                                                        <li><a href="knowledgebase.html">Knowledgebase</a></li>
                                                        <li><a href="login.html">Login</a></li>
                                                        <li><a href="register.html">register</a></li>
                                                        <li><a href="404.html">404 Not Found</a></li>
                                                    </ul>
                                                </li>
                                                <li><a href="#">Blog Pages<i class="fa fa-caret-right" aria-hidden="true"></i></a>
                                                    <ul class="sub-menu">
                                                        <li><a href="blog.html">Blog - 1</a></li>
                                                        <li><a href="blog-sidebar.html">Blog - 2</a></li>
                                                        <li><a href="single.html">Single Blog - 1</a></li>
                                                        <li><a href="single-sidebar.html">Single Blog - 2</a></li>
                                                    </ul>
                                                </li>
                                                <li><a href="#">Event Pages<i class="fa fa-caret-right" aria-hidden="true"></i></a>
                                                    <ul class="sub-menu">
                                                        <li><a href="event-grid.html">Event Grid</a></li>
                                                        <li><a href="event-list.html">Event List</a></li>
                                                        <li><a href="event-details.html">Event Details</a></li>
                                                    </ul>
                                                </li>
                                                <li><a href="#">Gallery Pages<i class="fa fa-caret-right" aria-hidden="true"></i></a>
                                                    <ul class="sub-menu">
                                                        <li><a href="gallery-fullwidth.html">Gallery Fullwidth</a></li>
                                                        <li><a href="gallery-4-column.html">Gallery 4 Column</a></li>
                                                        <li><a href="gallery-3-column.html">Gallery 3 Column</a></li>
                                                        <li><a href="gallery-2-column.html">Gallery 2 Column</a></li>
                                                    </ul>
                                                </li>
                                                <li><a href="#">Course Pages<i class="fa fa-caret-right" aria-hidden="true"></i></a>
                                                    <ul class="sub-menu">
                                                        <li><a href="course-grid.html">Course Grid</a></li>
                                                        <li><a href="course-list.html">Course List</a></li>
                                                        <li><a href="course-details.html">Course List</a></li>
                                                    </ul>
                                                </li>
                                                <li><a href="#">Teacher Pages<i class="fa fa-caret-right" aria-hidden="true"></i></a>
                                                    <ul class="sub-menu">
                                                        <li><a href="teachers.html">Teacher Grid</a></li>
                                                        <li><a href="teachers-details.html">Teacher Details</a></li>
                                                    </ul>
                                                </li>
                                                <li><a href="contact.html">Contact Page</a></li>
                                            </ul>
                                        </li>
                                        <li><a href="#">Gallery<i class="fa fa-caret-down" aria-hidden="true"></i></a>
                                            <ul class="sub-menu">
                                                <li><a href="gallery-fullwidth.html">Gallery Fullwidth</a></li>
                                                <li><a href="gallery-4-column.html">Gallery 4 Column</a></li>
                                                <li><a href="gallery-3-column.html">Gallery 3 Column</a></li>
                                                <li><a href="gallery-2-column.html">Gallery 2 Column</a></li>
                                            </ul>
                                        </li>
                                        <li><a href="#">course<i class="fa fa-caret-down" aria-hidden="true"></i></a>
                                            <ul class="sub-menu">
                                                <li><a href="course-grid.html">Course Grid</a></li>
                                                <li><a href="course-list.html">Course List</a></li>
                                                <li><a href="course-details.html">Course Details</a></li>
                                            </ul>
                                        </li>
                                        <li><a href="#">teacher<i class="fa fa-caret-down" aria-hidden="true"></i></a>
                                            <ul class="sub-menu">
                                                <li><a href="teachers.html">Teachers</a></li>
                                                <li><a href="teachers-details.html">Teacher Details</a></li>
                                            </ul>
                                        </li>
                                        <li><a href="#">Event<i class="fa fa-caret-down" aria-hidden="true"></i></a>
                                            <ul class="sub-menu">
                                                <li><a href="event-grid.html">Event Grid</a></li>
                                                <li><a href="event-list.html">Event List</a></li>
                                                <li><a href="event-details.html">Event Details</a></li>
                                            </ul>
                                        </li>
                                        <li><a href="contact.html">contact</a></li>
                                    </ul>
                                </nav>
                            </div>
                            <!-- mainmenu end -->
                            <!-- Search Button Area -->
                            <div class="search_button hidden-xs">
                                <a href="#"><i class="fa fa-search" aria-hidden="true"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Main Header Area End -->

        <!-- Search Box Area Start -->
        <div id="search">
            <div class="search_box_area">
                <form action="#" method="post">
                    <input type="text" name="s" id="search_box" placeholder="Enter keyword and hit enter">
                    <input type="submit" value="Submit" id="sub">
                    <div id="close_button">
                        <i class="fa fa-times-circle" aria-hidden="true"></i>
                    </div>
                </form>
            </div>
        </div>
        <!-- Search Box Area End -->
    </header>
    <!-- ===================== Header Area End ===================== -->

    <!-- ===================== Breadcumb area start ===================== -->
    <section class="breadcumb_area" style="background-image: url(img/bg-pattern/breadcumb.jpg);">
        <div class="container">
            <div class="row">
                <div class="col">
                    <div class="breadcumb_section">
                        <!-- Breadcumb page title start -->
                        <div class="page_title">
                            <h3>Student Profile</h3>
                        </div>
                        <!-- Breadcumb page pagination start -->
                        <div class="page_pagination">
                            <ul>
                                <li><a href="#">Home</a></li>
                                <li><i class="fa fa-angle-right" aria-hidden="true"></i></li>
                                <li>Student Profile</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- ===================== Breadcumb area end ===================== -->

    <!-- ================= All Our Teacher Area Start =============== -->
    <section class="all_our_teacher_area section_padding_100">
        <div class="container">
            <div class="row">
                <div class="col-md-6 col-12">
                    <!-- Teacher Full Image Start -->
                    <div class="student_full_image">
                        <?php
                        if (isset($data['photo'])){
                            echo '<img src="'.$data['photo'].'" alt="">';
                        }else{
                            echo'<img src="img/profiles/unknown.png" alt="">';
                        }
                        ?>
                        
                    </div>
                </div>
                <div class="col-md-6 col-12">
                    <!-- Teacher Details Info Area Start -->
                    <div class="teacher_details_info">
                        <!-- Teacher Name Designation Start -->
                        <div class="name_designation">
                            <h3><?php echo $data['name'];?></h3>
                            <?php
                            if (isset($data['nif'])){
                                echo '<h5>'.$data['nif'].'</h5>';
                            }
                            ?>
                            
                        </div>
                        <!-- About Teacher Start -->
                        <div class="about_teacher">
                            <p>This is your student profile section, where you can find your personal data from the University, as well as the completed degrees.</p>
                            <p>In this section, you can also download your completed education degree in your wallet.</p>
                        </div>
                        <!-- Teacher Contact Info Start -->
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
                                    <p>Software engineer (2017)</p>
                                </div>
                                <div class="contact_data">
                                    <button class="btn btn-default sign_in_vidchain btn-sm" id="validate-elicence" onclick="validateElicence(2, 'Software Engineer Degree', '<?php echo $data['token'];?>')"><img src="./img/icon-img/vidchain-ico.png" style="margin-right: 10px;" /> <strong>INCLUDE IN MY VIDCHAIN WALLET</strong><span class="glyphicon glyphicon-refresh spinning" style="margin-left: 10px;"></span></button>
                                </div>
                            </div>
                            
                            <!-- Single Contact Info Start -->
                            <div class="tea_single_contact_info">
                                <div class="contact_icon social">
                                    <a href="#"><i class="fa fa-facebook-official" aria-hidden="true"></i></a>
                                </div>
                                <div class="contact_icon social">
                                    <a href="#"><i class="fa fa-twitter" aria-hidden="true"></i></a>
                                </div>
                                <div class="contact_icon social">
                                    <a href="#"><i class="fa fa-google-plus" aria-hidden="true"></i></a>
                                </div>
                                <div class="contact_icon social">
                                    <a href="#"><i class="fa fa-pinterest" aria-hidden="true"></i></a>
                                </div>
                                <div class="contact_icon social">
                                    <a href="#"><i class="fa fa-youtube" aria-hidden="true"></i></a>
                                </div>
                            </div>
                        </div>
                        <!-- Teacher Contact Info End -->
                    </div>
                    <!-- Teacher Details Info Area End -->
                </div>
            </div>
        </div>
    </section>
    <!-- ===================== All Our Teacher Area End ==================== -->

    <!-- ===================== Cool Facts Area Start ===================== -->
    <section class="cool_facts_area section_padding_100_70">
        <div class="container">
            <div class="row">
                <div class="col-12 col-sm-3">
                    <!-- Single Cool Facts area Start -->
                    <div class="cool_fact_text">
                        <i class="fa fa-book" aria-hidden="true"></i>
                        <h3><span class="counter">763</span></h3>
                        <h5>Free Courses</h5>
                    </div>
                    <!-- Single Cool Facts area End -->
                </div>

                <div class="col-12 col-sm-3">
                    <!-- Single Cool Facts area Start -->
                    <div class="cool_fact_text">
                        <i class="fa fa-users" aria-hidden="true"></i>
                        <h3><span class="counter">10</span>k+</h3>
                        <h5>STUDENTS ENROLLED</h5>
                    </div>
                    <!-- Single Cool Facts area End -->
                </div>

                <div class="col-12 col-sm-3">
                    <!-- Single Cool Facts area Start -->
                    <div class="cool_fact_text">
                        <i class="fa fa-check-square-o" aria-hidden="true"></i>
                        <h3><span class="counter">251</span></h3>
                        <h5>CERTIFIED TEACHERS</h5>
                    </div>
                    <!-- Single Cool Facts area End -->
                </div>

                <div class="col-12 col-sm-3">
                    <!-- Single Cool Facts area Start -->
                    <div class="cool_fact_text">
                        <i class="fa fa-graduation-cap" aria-hidden="true"></i>
                        <h3><span class="counter">7412</span></h3>
                        <h5>Complate Graduates</h5>
                    </div>
                    <!-- Single Cool Facts area End -->
                </div>

            </div>
        </div>
    </section>
    <!-- ===================== Why Chooses Area End ===================== -->

    <!-- ===================== Our Teacher Area Start ===================== -->
    <section class="our_teachers_area section_padding_100">
        <div class="container">
            <div class="row">
                <div class="col">
                    <div class="section_heading">
                        <img src="img/teacher-img/teach-icon.png" alt="">
                        <h4>Our Others Teachers</h4>
                    </div>
                </div>
            </div>
            <div class="row">

                <div class="col-12 col-md-3">
                    <div class="single_teacher_profile">
                        <div class="teacher_thumb">
                            <img src="img/teacher-img/team-member-1.jpg" alt="">
                        </div>
                        <div class="single_teacher_details_info">
                            <h5>NAZRUL ISLAM</h5>
                            <p>Senior Teacher</p>
                            <div class="teacher_social_info">
                                <div class="social_icon">
                                    <a href="#"><i class="fa fa-facebook"></i></a>
                                    <a href="#"><i class="fa fa-twitter"></i></a>
                                    <a href="#"><i class="fa fa-skype"></i></a>
                                    <a href="#"><i class="fa fa-dribbble"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-12 col-md-3">
                    <div class="single_teacher_profile">
                        <div class="teacher_thumb">
                            <img src="img/teacher-img/team-member-2.jpg" alt="">
                        </div>
                        <div class="single_teacher_details_info">
                            <h5>DELOWAR HOSAIN</h5>
                            <p>Senior Teacher</p>
                            <div class="teacher_social_info">
                                <div class="social_icon">
                                    <a href="#"><i class="fa fa-facebook"></i></a>
                                    <a href="#"><i class="fa fa-twitter"></i></a>
                                    <a href="#"><i class="fa fa-skype"></i></a>
                                    <a href="#"><i class="fa fa-dribbble"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-12 col-md-3">
                    <div class="single_teacher_profile">
                        <div class="teacher_thumb">
                            <img src="img/teacher-img/team-member-3.jpg" alt="">
                        </div>
                        <div class="single_teacher_details_info">
                            <h5>MITHILA MOU</h5>
                            <p>Senior Teacher</p>
                            <div class="teacher_social_info">
                                <div class="social_icon">
                                    <a href="#"><i class="fa fa-facebook"></i></a>
                                    <a href="#"><i class="fa fa-twitter"></i></a>
                                    <a href="#"><i class="fa fa-skype"></i></a>
                                    <a href="#"><i class="fa fa-dribbble"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-12 col-md-3">
                    <div class="single_teacher_profile">
                        <div class="teacher_thumb">
                            <img src="img/teacher-img/team-member-4.jpg" alt="">
                        </div>
                        <div class="single_teacher_details_info">
                            <h5>IMRAN KHAN</h5>
                            <p>Senior Teacher</p>
                            <div class="teacher_social_info">
                                <div class="social_icon">
                                    <a href="#"><i class="fa fa-facebook"></i></a>
                                    <a href="#"><i class="fa fa-twitter"></i></a>
                                    <a href="#"><i class="fa fa-skype"></i></a>
                                    <a href="#"><i class="fa fa-dribbble"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>
    <!-- ===================== Our Teacher Area End ===================== -->

     <!-- ===================== Newsletter Area Start ===================== -->
    <div class="newsletter_area wow fadeInUp">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <div class="newsletter_text">
                        <h4>Subcribe weekly newsletter</h4>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="newsletter_from">
                        <form action="#">
                            <div class="form-group">
                                <input type="email" class="form-control" id="email" placeholder="Enter Your E-mail" required>
                            </div>
                            <button type="submit" class="btn btn-default"><i class="fa fa-paper-plane"></i>Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- ===================== Newsletter Area End ===================== -->

    <!-- ===================== Footer Area Start ===================== -->
    <footer class="footer_area">
        <div class="container section_padding_100_70">
            <div class="row">
                <!-- Footer About Area Start -->
                <div class="col-12 col-md-6 col-lg-3">
                    <div class="footer_about_us footer-single-part item wow fadeInUp">
                        <div class="title">
                            <h4>About EduCamp</h4>
                            <!-- Useful Links Title -->
                            <div class="underline"></div>
                        </div>
                        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut delectus consectetur omnis, alias nulla repudiandae quasi non at ullam, vel officiis unde cum ea. Perferendis tempora eligendi aut, repellat eius. Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
                    </div>
                </div>
                <!-- Footer About Area End -->

                <!-- Upcoming Area Start -->
                <div class="col-12 col-md-6 col-lg-3">
                    <div class="footer_upcoming_event footer-single-part item wow fadeInUp">
                        <div class="title">
                            <h4>Upcoming event</h4>
                            <!-- Useful Links Title -->
                            <div class="underline"></div>
                        </div>
                        <!-- Single upcoming post -->
                        <div class="event_single_post">
                            <a href="#">
                                <p>Improve Your Computer Skills, Sign Up For Free Online Courses</p>
                            </a>
                        </div>
                        <!-- Single upcoming post -->
                        <div class="event_single_post">
                            <a href="#">
                                <p>Improve Your Computer Skills, Sign Up For Free Online Courses</p>
                            </a>
                        </div>
                        <!-- Single upcoming post -->
                        <div class="event_single_post">
                            <a href="#">
                                <p>Improve Your Computer Skills, Sign Up For Free Online Courses</p>
                            </a>
                        </div>
                    </div>
                </div>
                <!-- Upcoming Area End -->

                <!-- Contact info Area Start -->
                <div class="col-12 col-md-6 col-lg-3">
                    <div class="footer_contact_info footer-single-part item wow fadeInUp">
                        <div class="title">
                            <h4>get in touch</h4>
                            <!-- Useful Links Title -->
                            <div class="underline"></div>
                        </div>
                        <!-- single contact info start -->
                        <div class="footer_single_contact_info">
                            <i class="fa fa-thumb-tack" aria-hidden="true"></i>
                            <p>House - 87, Mirpur DOHS, Dhaka, Bangladesh</p>
                        </div>
                        <!-- single contact info start -->
                        <div class="footer_single_contact_info">
                            <i class="fa fa-phone" aria-hidden="true"></i>
                            <a href="tel:+8801791166123">+88 017 911 66123</a>
                            <a href="tel:+8801791166123">+88 017 911 66123</a>
                        </div>
                        <!-- single contact info start -->
                        <div class="footer_single_contact_info">
                            <i class="fa fa-envelope-o" aria-hidden="true"></i>
                            <a href="mailto:info@educamp.com">info@educamp.com</a>
                            <a href="mailto:care@educamp.com">care@educamp.com</a>
                        </div>
                    </div>
                </div>
                <!-- Contact info Area End -->

                <!-- Useful Links Area Start -->
                <div class="col-12 col-md-6 col-lg-3">
                    <div class="important_links footer-single-part item wow fadeInUp">
                        <div class="title">
                            <h4>useful links</h4>
                            <!-- Useful Links Title -->
                            <div class="underline"></div>
                        </div>
                        <!-- Links Start -->
                        <div class="links">
                            <p><i class="fa fa-angle-double-right" aria-hidden="true"></i><a href="#">All Our Courses</a></p>
                            <p><i class="fa fa-angle-double-right" aria-hidden="true"></i><a href="#">Event Calendar</a></p>
                            <p><i class="fa fa-angle-double-right" aria-hidden="true"></i><a href="#">Customer Support</a></p>
                            <p><i class="fa fa-angle-double-right" aria-hidden="true"></i><a href="#">Career at EduCamp</a></p>
                            <p><i class="fa fa-angle-double-right" aria-hidden="true"></i><a href="#">Terms &amp; Conditions</a></p>
                            <p><i class="fa fa-angle-double-right" aria-hidden="true"></i><a href="#">Community Forums</a></p>
                        </div>
                        <!-- Links End -->
                    </div>
                </div>
                <!-- Useful Links Area End -->
            </div>
        </div>

        <!-- Bottom Footer Area Start -->
        <div class="footer_bottom_area">
            <div class="container">
                <div class="row">
                    <div class="col">
                        <div class="footer_bottom wow fadeInDown">
                            <p>Made with <i class="fa fa-heart" aria-hidden="true"></i> by <a href="#">Designing World</a></p>
                        </div>
                        <!-- Bottom Footer Copywrite Text Area End -->
                    </div>
                </div>
            </div>
        </div>
        <!-- Bottom Footer Area End -->
    </footer>
    <!-- ===================== Footer Area End ===================== -->

    <!-- ===================== All jQuery Plugins ===================== -->

    <!-- jQuery (necessary for all JavaScript plugins) -->
    <script src="js/jquery-2.2.4.min.js"></script>
    <!-- Tether js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
    <!-- Bootstrap js -->
    <script src="js/bootstrap.min.js"></script>

    <script src="//rawgit.com/saribe/eModal/master/dist/eModal.min.js"></script>
    <!-- Plugins js -->
    <script src="js/plugins.js"></script>
    <!-- Active js -->
    <script src="js/custom.js"></script>

    <script src="../assets/js/fake-login-success.js"></script>

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
                       <p>Please, check your ViDChain APP in order to include your degree in your ViDChain Wallet</p>                                                   
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