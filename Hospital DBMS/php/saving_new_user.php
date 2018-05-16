<html>
    <?php
        echo'<link rel="stylesheet" type="text/css" href="/final_project_630/css/commons.css"/>';
        $patient_id = (int)$_POST['patient_id'];
        $name = $_POST["name_of_patient"];
        $address = $_POST["address"];
        $phone = $_POST["phone"];
        $dob = $_POST["dob"];
        if(isset($_POST["gender"]))
            $gender = $_POST["gender"];
        $conn = new mysqli("localhost", "root", "root");
//        $result = $conn->query($sql);
//        if ($result->num_rows > 0) {
//            // output data of each row
//            while($row = $result->fetch_assoc()) {
//                echo "id: " . $row["Hospital_ID"]."<br>";
//            }
//        } else {
//            echo "0 results";
//        }
        $sql = "insert into mydb.patient_info (patient_id, patient_name, address, contact_no, gender, dob)
            values (".$patient_id.",'".$name."','".$address."','".$phone."','".$gender."','".$dob."')";
        if ($conn->query($sql)) {
            echo "User Created <br>";
            echo "<a href='/final_project_630/index.php' class='button'>Go to Home Page</a> 
                <a href='create_user_form.html' class='button'>Create another user</a>";
        }
        mysqli_close($conn);    
    /*
     * To change this template, choose Tools | Templates
     * and open the template in the editor.
     */
    ?>
</html>
