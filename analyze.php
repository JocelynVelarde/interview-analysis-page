<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $analysisOption = $_POST["analysisOption"];
    $fileContent = file_get_contents($_FILES["file"]["tmp_name"]);
    
    $pythonScript = "python3 int/reversedgpt.py"; // Reemplaza con la ruta correcta
    $command = escapeshellcmd("$pythonScript $analysisOption " . escapeshellarg($fileContent));
    $output = shell_exec($command);

    // Envía la respuesta de vuelta a la página web
    echo $output;
    
    // Llama a tu script de chatbot en Python y pasa los datos
}
?>
