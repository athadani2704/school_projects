<?php
    $user = $_GET["user"];
    $conn = new mysqli("localhost", "root", "root");
    $sql = "select patient_id, patient_name, contact_no from mydb.patient_info
        where patient_id like '%".$user."%' or patient_name like '%".$user."%'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $out = "<table><tr><th>Patient ID</th><th>Patient Name</th><th>Contact No.</th></tr>";
        while($row = $result->fetch_assoc()) {
            $out .= "<tr>";
            $out .= "<td>".$row["patient_id"]."</td>
                <td><a href=edit_user.php?user=".$row["patient_id"].">".$row["patient_name"]."</a></td>
                <td>".$row["contact_no"]."</td>";
            $out .= "</tr>";
        }
        $out .= "</table>";
        echo $out;
    }
    else {
        echo "No such user exists";
    }
    mysqli_close($conn);
/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
?>
