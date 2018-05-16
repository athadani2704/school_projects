<?php
    echo'<link rel="stylesheet" type="text/css" href="/final_project_630/css/commons.css"/>';
    $user = (int)$_POST["user_id"];
    $conn = new mysqli("localhost", "root", "root");
    $sql = "delete from mydb.revenue_management_system where transaction_id in 
            (select transaction_id from mydb.patient_registration where patient_id = ".$user.");";
    $sql .= "delete from mydb.patient_registration where patient_id = ".$user.";";
    $sql .= "delete from mydb.patient_info where patient_id = ".$user.";";
    
    if (mysqli_multi_query($conn, $sql)) {
        echo "User Deleted<br>";
        echo "<a href='/final_project_630/index.php' class='button'>Go to Home Page</a>";
    }
    else {
        echo "Error deleting record: " . $conn->error;
    }
    mysqli_close($conn);    
    
/* 
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
?>
