<?php
    echo'<link rel="stylesheet" type="text/css" href="/final_project_630/css/commons.css"/>';
    $user_id = $_GET["user"];
    $conn = new mysqli("localhost", "root", "root");
    $sql = "select patient_name, address, contact_no, gender, dob from mydb.patient_info
        where patient_id = ".$user_id;
    $result = $conn->query($sql);
    echo "<script>function redirect(){
        window.location = 'search_user.html';}</script>";
    echo "<h1 style='text-align:center'>PatientID:".$user_id."</h1>";
    echo "<form action='delete_user.php' method='post'>
        <input type='text' value='".$user_id."' name= 'user_id' hidden/>
        <input type='submit' value='Delete this user' class='button'/>
        </form>";
    if ($result->num_rows > 0) {
        $out = "";
        $out .= "<form action='updating_user.php' method='post'/>";
        while($row = $result->fetch_assoc()) {
            $out .= "<input type='text' value='".$user_id."' hidden name='user_id' class='text'/><br>";
            $out .= "Name: <input type='text' value='".$row["patient_name"]."' name='patient_name' class='text'/><br>";
            $out .= "Contact No.: <input type='number' value='".$row["contact_no"]."' name='contact_no' class='text'/><br>";
            $out .= "Address: <input type='text' name='address' class='text' value='".$row["address"]."'/><br>";
            $out .= "Gender: ".$row["gender"]."<br>DOB: ".$row["dob"]."<br>";
            $out .= "<input type='submit' value='save' class='button'/></form>";
        }
        echo $out;
    }

    echo "<div style='text-align:center;'><input type='button' value='Go back to searching' class='button'
        onclick='redirect()'/></div>";
    
    $sql = "select a.transaction_id, b.procedure_name, a.prescription, a.check_in, a.check_out, a.cost_of_bill
            from mydb.patient_registration a, mydb.procedure_table b where
            a.patient_id =".$user_id." and a.procedure_id = b.procedure_id";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $out = "<div><table><tr><th>Transaction ID</th><th>Procedure</th><th>Prescription</th>";
        $out .= "<th>Check In</th><th>Check Out</th><th>Cost of Bill</th></tr>";
        while($row = $result->fetch_assoc()) {
            $out .= "<tr>";
            $out .= "<td>".$row['transaction_id']."</td>";
            $out .= "<td>".$row['procedure_name']."</td>";
            $out .= "<td>".$row['prescription']."</td>";
            $out .= "<td>".$row['check_in']."</td>";
            $out .= "<td>".$row['check_out']."</td>";
            $out .= "<td>".$row['cost_of_bill']."</td>";
            $out .= "</tr>";
        }
        $out .= "</table></div>";
        echo $out;
    }
    mysqli_close($conn);
/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
?>