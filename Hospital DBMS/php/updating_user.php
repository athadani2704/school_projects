<?php
    echo'<link rel="stylesheet" type="text/css" href="/final_project_630/css/commons.css"/>';
    $user_id = $_POST["user_id"];
    $patient_name = $_POST["patient_name"];
    $contact_no = $_POST["contact_no"];
    $address = $_POST["address"];
    $conn = new mysqli("localhost", "root", "root");
    $sql = "update mydb.patient_info set patient_name = '".$patient_name."',
        address = '".$address."', contact_no = '".$contact_no."' where patient_id = ".$user_id;
    if ($conn->query($sql)) {
    echo "Changes saved <br>";
    echo "<a href='/final_project_630/index.php' class='button'>Go to Home Page</a> <a href='create_user_form.html' class='button'>Create another user</a>";
    }
    mysqli_close($conn);    
    
/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
?>
