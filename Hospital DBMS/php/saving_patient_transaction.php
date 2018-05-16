<?php   //get transaction id from database and proc id from procedure table using procedure name
        echo'<link rel="stylesheet" type="text/css" href="/final_project_630/css/commons.css"/>';
        $patient_id = (int)$_POST["patient_id"];
        $procedure_id = $_POST["procedure_id"];
        $prescription = $_POST["prescription"];
        $check_in = $_POST["check_in"];
        $check_out = $_POST["check_out"];
        $cost_of_bill = (float)$_POST["cost_of_bill"];
        $hospital_id = (int)$_POST["hospital_id"];
        $third_party = (int)$_POST["third_party_service"];
        $conn = new mysqli("localhost", "root", "root");

        $transaction_id = "select max(transaction_id) as T from mydb.patient_registration";
        $result = $conn->query($transaction_id);
        
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                $transaction_id = (int)$row["T"];
                $transaction_id += 1;
            }
        }
        $sql = "insert into mydb.patient_registration 
            (transaction_id, patient_id, procedure_id, prescription, cost_of_bill, hospital_id, check_in, check_out)
            values (".$transaction_id.",".$patient_id.",'".$procedure_id."','".$prescription."',".$cost_of_bill.",".
                $hospital_id.",'".$check_in."','".$check_out."');";
        
        $sql .= "insert into mydb.revenue_management_system (transaction_id, revenue_generated, service_id)
            values (".$transaction_id.",".$cost_of_bill.",".$third_party.");";
        mysqli_multi_query($conn, $sql);
        echo "Transaction entered <br>";
        echo "<a href='/final_project_630/index.php' class='button'>Go to Home Page</a> <a href='patient_registration.html' class='button'>Create another transaction</a>";
        mysqli_close($conn);    
    /*
     * To change this template, choose Tools | Templates
     * and open the template in the editor.
     */

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
?>
