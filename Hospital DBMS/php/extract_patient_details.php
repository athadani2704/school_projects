<?php
    $id = (int)$_GET["my_id"];
    
    $conn = new mysqli("localhost", "root", "root");
    
    $sql = "select patient_name, address, contact_no from mydb.patient_info where patient_id=".$id;
    $result = $conn->query($sql);
    $out = "";
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $out = $row["patient_name"]."/".$row["contact_no"]."/".$row["address"];
        }
    }
    else $out = "No such user";
    
    echo $out;
    mysqli_close($conn); 
/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
?>
