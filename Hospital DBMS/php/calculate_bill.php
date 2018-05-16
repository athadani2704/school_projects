<?php
    $proc = $_GET["proc"];
    $third_party = (int)$_GET["third_party"];
    
    $conn = new mysqli("localhost", "root", "root");
    
    $sql = "select cost_of_proc from mydb.procedure_table where procedure_id='".$proc."'";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $proc = $row["cost_of_proc"];
        }
    }
    $sql = "select cost_incurred from mydb.third_party_table where service_id=".$third_party;
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $third_party = $row["cost_incurred"];
        }
    }
    
    echo ($proc + $third_party);
    mysqli_close($conn);     
/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
?>
