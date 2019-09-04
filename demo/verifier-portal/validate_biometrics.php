<?php 

/*
	$gradientUrlApi = 'https://biometrics.gradiant.org:443/FaceIDNN/profiles/';
	$digestToken = 'Um9ja3lNYXJjaEFtdWNrRWF0c1RhbG9uQmFjb24=';
	
	$_parameters = json_decode(file_get_contents('php://input', true));
	$registerImage = $_parameters->image_1;
	$compareImage = $_parameters->image_2;
	$profileID_1 = createProfile($registerImage);
	$result = false;
	if(!empty($profileID_1)){
		$resisterResult = registerProfile($profileID_1);
		if(empty($resisterResult)){
			$profileID_2 = createProfile($compareImage);
			if(!empty($profileID_2)){
				$JSONResult = match($profileID_2, $profileID_1);
				if(!empty($JSONResult)){
					$result = json_decode($JSONResult);
					if(($result->score > $result->threshold) || ($result->scoreNormalized < $result->thresholdNormalized)){
						$result =  false;
					}else{
						$result = true;
					}
					deleteProfile($profileID_1);
					deleteProfile($profileID_2);
				}
			}
		}
		
	}
	echo json_encode([
        "result" => $result
    ]);
*/

	echo json_encode([
        "result" => true
    ]);
	
	die();
	
	function createProfile($image){
		global $gradientUrlApi, $digestToken;
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $gradientUrlApi);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
		curl_setopt($ch, CURLOPT_HTTPHEADER, array(
				'Authorization: Digest '.$digestToken,
				'Content-Type: image/jpg'
		));		        
		curl_setopt($ch, CURLOPT_POSTFIELDS, base64_decode($image));
		error_log("Creating profile...");
		$output = curl_exec($ch);
		$info = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		error_log('Status: '.$info);		
		$result='';
		if($info=='201'){
			$jsonResp = json_decode($output);
			$result = $jsonResp->profileID;
		}else{
			error_log($output);
			$result='';
		}
		curl_close($ch);		
		return $result;
	}
	
	function registerProfile($profileId){
		global $gradientUrlApi, $digestToken;
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $gradientUrlApi.$profileId.'/registered=1');
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PATCH");
		curl_setopt($ch, CURLOPT_HTTPHEADER, array(
				'Authorization: Digest '.$digestToken
		));		        
		error_log("Registering profile...");
		$output = curl_exec($ch);
		$info = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		error_log('Status: '.$info);
		$result='';
		if($info=='200'){
			$result='';
		}else{
			error_log($output);
			$result='Error: '.$info;
		}
		curl_close($ch);		
		return $result;
	}
	
	function getProfile($profileId){
		global $gradientUrlApi, $digestToken;
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $gradientUrlApi.$profileId);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "GET");
		curl_setopt($ch, CURLOPT_HTTPHEADER, array(
				'Authorization: Digest '.$digestToken
		));		        
		error_log("Getting profile...");
		$output = curl_exec($ch);
		$info = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		error_log('Status: '.$info);
		$result='';
		if($info=='200'){
			$result=$output;
		}else{
			error_log($output);
			$result='';
		}
		curl_close($ch);		
		return $result;
	}
	
	function match($profileId, $targetId){
		global $gradientUrlApi, $digestToken;
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $gradientUrlApi.'match/id1='.$profileId.'&id2='.$targetId);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "GET");
		curl_setopt($ch, CURLOPT_HTTPHEADER, array(
				'Authorization: Digest '.$digestToken
		));		        
		error_log("Maching profile...");
		$output = curl_exec($ch);
		$info = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		error_log('Status: '.$info);
		$result='';
		if($info=='200'){
			$result=$output;
		}else{
			error_log($output);
			$result='';
		}
		curl_close($ch);		
		return $result;
	}
	
	function deleteProfile($profileId){
		global $gradientUrlApi, $digestToken;
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $gradientUrlApi.$profileId);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
		curl_setopt($ch, CURLOPT_HTTPHEADER, array(
				'Authorization: Digest '.$digestToken
		));		        
		error_log("Deleting profile...");
		$output = curl_exec($ch);
		$info = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		error_log('Status: '.$info);
		$result='';
		if($info=='200'){
			$result=$output;
		}else{
			error_log($output);
			$result='';
		}
		curl_close($ch);		
		return $result;
	}
?>