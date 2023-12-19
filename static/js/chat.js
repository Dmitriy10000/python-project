var searchTimeout;

// Выполняем запрос на получение списка пользователей по фильтру
function globalSearch() {
	clearTimeout(searchTimeout);
	searchTimeout = setTimeout(function () {
		var searchQuery = document.getElementById('globalSearchInput').value;
		
		// Очищаем предыдущие результаты поиска
		document.getElementById('searchResults').innerHTML = '';

		// Не отправляем searchQuery если он пустой
		if (searchQuery == '') {
			return;
		}
		fetch('/global_user_search', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			},
			body: new URLSearchParams({
				search_query: searchQuery,
			}),
		})
		.then(response => response.json())
		.then(data => {
			console.log('Success:', data);

			// Обрабатываем результаты поиска
			var resultsContainer = document.getElementById('searchResults');
			data.forEach(user => {
				var listItem = document.createElement('div');
				listItem.classList.add('search_result');
				listItem.innerHTML = `
					<div class="us_logo">
						<img src="static/icons/us_logo.png" alt=""></img>
					</div>
					<div class="us_name">${user.name} ${user.surname}</div>
				`;
				var buttonsContainer = document.createElement('div');
				buttonsContainer.classList.add('buttons');
				buttonsContainer.innerHTML += `<button id="pm ${user.user_id}" class="pm" onclick="personalMessages(${user.user_id})"><svg class="pm_icon" width="2em" height="2em" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M23.7994 18.3704L23.8013 18.373C24.1307 18.8032 24.2888 20.2316 22.0258 19.9779C21.3596 19.9033 20.4282 19.7715 19.3088 19.3471C18.5551 19.0613 17.8986 18.7026 17.3584 18.3522C16.4699 18.7098 15.5118 18.9296 14.5113 18.9857C13.1436 20.8155 10.9602 22 8.50001 22C7.69152 22 6.91135 21.8717 6.17973 21.6339C5.74016 21.8891 5.24034 22.1376 4.68789 22.3471C3.56851 22.7715 2.63949 22.9297 1.97092 22.9779C1.47028 23.014 1.11823 22.9883 0.944098 22.9681C0.562441 22.9239 0.219524 22.7064 0.072134 22.3397C-0.0571899 22.0179 -0.0104055 21.6519 0.195537 21.3728C0.448192 21.0283 0.680439 20.6673 0.899972 20.3011C1.32809 19.5868 1.74792 18.8167 1.85418 17.9789C1.30848 16.9383 1.00001 15.7539 1.00001 14.5C1.00001 11.5058 2.75456 8.92147 5.29159 7.71896C6.30144 3.85296 9.81755 1 14 1C18.9706 1 23 5.02944 23 10C23 11.3736 22.6916 12.6778 22.1395 13.8448C21.9492 15.5687 22.8157 17.0204 23.7994 18.3704ZM7.00001 10C7.00001 6.13401 10.134 3 14 3C17.866 3 21 6.13401 21 10C21 11.1198 20.7378 12.1756 20.2723 13.1118C20.2242 13.2085 20.1921 13.3124 20.1772 13.4194C19.9584 14.9943 20.3278 16.43 21.0822 17.8083C19.9902 17.5451 18.9611 17.0631 18.0522 16.4035C17.7546 16.1875 17.3625 16.1523 17.0312 16.3117C16.1152 16.7525 15.0879 17 14 17C10.134 17 7.00001 13.866 7.00001 10ZM5.00353 10.2543C5.11889 14.4129 8.05529 17.8664 11.9674 18.7695C11.0213 19.5389 9.8145 20 8.50001 20C7.7707 20 7.07689 19.8586 6.44271 19.6026C6.14147 19.481 5.79993 19.5133 5.52684 19.6892C5.08797 19.972 4.56616 20.2543 3.9788 20.477C3.58892 20.6248 3.23263 20.7316 2.91446 20.8083C3.24678 20.2012 3.58332 19.4779 3.73844 18.7971C3.81503 18.461 3.8572 18.1339 3.87625 17.8266C3.88848 17.6293 3.84192 17.4327 3.74245 17.2618C3.27058 16.451 3.00001 15.5086 3.00001 14.5C3.00001 12.7904 3.78 11.263 5.00353 10.2543Z"/></svg></button></div>`;
				if (user.is_friend == false) {
					buttonsContainer.innerHTML += `<button id="add ${user.user_id}" class="add" onclick="addToFriendList(${user.user_id})"><svg class="icon" width="2em" height="2em" viewBox="0 0 1000 1000" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"  enable-background="new 0 0 1000 1000" xml:space="preserve"><g><g transform="translate(0.000000,512.000000) scale(0.100000,-0.100000)"><path d="M2704.2,4987.1c-34.5-34.5-36.4-57.4-28.7-245.1c24.9-505.5,34.5-988,23-1020.6c-24.9-68.9-95.7-65.1-245.1,9.6c-130.2,65.1-139.8,67-183.8,38.3c-24.9-15.3-46-46-46-67c0-21.1,53.6-281.5,118.7-580.2l118.7-540l11.5-651l11.5-651l90-268.1c162.8-478.7,344.7-781.2,633.8-1058.9c86.2-82.4,222.1-191.5,304.4-243.2l149.4-93.8l-13.4-97.6c-5.7-51.7-15.3-101.5-19.1-107.2c-3.8-7.6-134-17.2-289.1-23c-162.7-5.8-327.4-23-388.7-40.2c-162.8-45.9-361.9-155.1-484.4-266.1c-151.3-137.9-1106.7-1401.6-1192.9-1577.8c-97.7-199.1-122.5-365.7-122.5-802.3c0-430.8,24.9-597.4,124.5-802.3c74.7-155.1,183.8-293,321.7-405.9c99.6-82.3,291-187.6,382.9-208.7l51.7-11.5v407.8c0,226,9.6,442.3,19.2,480.6c24.9,88.1,126.4,178.1,218.3,195.3c107.2,21.1,227.8-44.1,277.6-149.4c36.4-74.7,40.2-114.9,40.2-534.2V-4780h1876.4h1876.4v474.9c0,434.6,3.8,478.7,38.3,534.2c74.7,124.5,201,162.8,333.2,103.4c158.9-68.9,164.7-91.9,164.7-637.6V-4780l63.2,11.5c285.3,49.8,520.8,170.4,704.6,365.7c147.4,157,208.7,256.6,279.6,457.6c53.6,149.4,53.6,155.1,53.6,630c0,409.8-5.7,494-34.5,591.7c-51.7,164.7-132.1,314-243.2,453.8l-97.6,120.6l-329.4,1.9c-298.7,1.9-344.6,7.6-497.8,53.6c-698.9,214.5-1166.1,723.8-1319.3,1439.9c-40.2,189.6-28.7,562.9,21.1,765.9c49.8,195.3,155.1,432.7,264.2,597.4c164.7,248.9,497.8,536.1,752.5,647.2c47.9,21.1,91.9,46,99.6,57.4c7.6,9.6,15.3,394.4,13.4,852.1c0,917.2-9.6,1041.6-109.1,1250.3c-151.3,323.6-419.3,545.7-760.2,635.7c-91.9,23-250.8,28.7-871.2,30.6h-756.3l-170.4,220.2c-93.8,120.6-189.6,233.6-214.5,248.9c-57.4,38.3-113,9.6-151.3-78.5c-24.9-63.2-51.7-78.5-122.5-67c-15.3,1.9-122.5,82.3-239.3,180C2771.2,5052.2,2769.3,5052.2,2704.2,4987.1z"/><path d="M7154.1,1209.3c-93.8-34.5-160.8-90-206.8-174.2c-40.2-76.6-42.1-107.2-47.9-553.4l-7.7-472.9L6409.2,3c-474.8-5.7-484.4-5.7-551.4-51.7C5608.9-221,5645.3-575.2,5922.9-692c57.4-23,158.9-28.7,520.8-28.7h448l7.7-472.9c5.7-517,9.6-534.2,124.5-639.5c80.4-76.6,126.4-93.8,239.3-93.8c124.5,0,212.5,42.1,291.1,139.8l59.3,74.7l5.7,495.9l5.7,495.9h459.5c490.2,0,545.7,9.6,647.2,101.5c61.3,57.4,116.8,180,116.8,262.3c0,134-113,296.8-235.5,342.7c-32.6,13.4-237.4,21.1-520.8,21.1h-467.2l-5.7,494c-5.7,492.1-5.7,495.9-53.6,564.9c-55.5,82.3-208.7,166.6-294.9,164.7C7238.3,1230.4,7186.6,1220.8,7154.1,1209.3z"fill="#4BD295";/></g></g></svg></button>`;
				}
				else if (user.is_invite_sent == true) {
					buttonsContainer.innerHTML += `<button id="add ${user.user_id}" class="cancel_request" onclick="cancelRequest(${user.user_id})"><svg width="25px" height="25px" viewBox="0 0 1024 1024" class="icon"  version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M704 288h-281.6l177.6-202.88a32 32 0 0 0-48.32-42.24l-224 256a30.08 30.08 0 0 0-2.24 3.84 32 32 0 0 0-2.88 4.16v1.92a32 32 0 0 0 0 5.12A32 32 0 0 0 320 320a32 32 0 0 0 0 4.8 32 32 0 0 0 0 5.12v1.92a32 32 0 0 0 2.88 4.16 30.08 30.08 0 0 0 2.24 3.84l224 256a32 32 0 1 0 48.32-42.24L422.4 352H704a224 224 0 0 1 224 224v128a224 224 0 0 1-224 224H320a232 232 0 0 1-28.16-1.6 32 32 0 0 0-35.84 27.84 32 32 0 0 0 27.84 35.52A295.04 295.04 0 0 0 320 992h384a288 288 0 0 0 288-288v-128a288 288 0 0 0-288-288zM103.04 760a32 32 0 0 0-62.08 16A289.92 289.92 0 0 0 140.16 928a32 32 0 0 0 40-49.92 225.6 225.6 0 0 1-77.12-118.08zM64 672a32 32 0 0 0 22.72-9.28 37.12 37.12 0 0 0 6.72-10.56A32 32 0 0 0 96 640a33.6 33.6 0 0 0-9.28-22.72 32 32 0 0 0-10.56-6.72 32 32 0 0 0-34.88 6.72A32 32 0 0 0 32 640a32 32 0 0 0 2.56 12.16 37.12 37.12 0 0 0 6.72 10.56A32 32 0 0 0 64 672z" /></svg></button>`;
				}
				else if (user.is_invite_received == true) {
					buttonsContainer.innerHTML += `<button id="accept ${user.user_id}" class="accept_request" onclick="acceptRequest(${user.user_id})"><svg fill="#000000" width="2em" height="2em" viewBox="0 0 1000 1000" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"  enable-background="new 0 0 1000 1000" xml:space="preserve"><g><g transform="translate(0.000000,512.000000) scale(0.100000,-0.100000)"><path d="M2262.7,4985c-30.6-30.6-34.5-57.4-26.8-204.8c26.8-566.6,36.4-1018.4,23-1054.8c-26.8-74.7-95.7-72.7-245,3.8c-130.2,68.9-137.8,68.9-183.8,40.2c-26.8-17.2-47.9-47.9-47.9-67c0-21,53.6-275.6,118.7-570.5l116.8-532.2l13.4-660.4l11.5-660.4l90-266.1c206.8-606.9,516.9-1035.7,945.7-1307.5c141.7-90,143.6-91.9,132.1-158.9c-5.7-36.4-11.5-86.1-11.5-107.2c0-40.2-11.5-42.1-291-51.7C2592-624,2475.2-647,2289.5-738.8c-231.6-114.9-312-201-863.4-928.4c-287.1-377.1-543.7-727.4-568.6-775.3c-26.8-47.9-68.9-147.4-93.8-222.1c-42.1-126.3-44-160.8-44-631.7c0-490.1,1.9-499.6,53.6-652.8c86.1-260.4,262.3-488.2,486.2-631.7c93.8-61.3,271.8-141.7,312-141.7c11.5,0,19.1,158.9,19.1,407.8c0,222.1,9.6,438.4,19.1,476.7c24.9,88,126.3,178,218.2,195.3c107.2,21.1,227.8-44,277.6-149.3c36.4-74.7,40.2-114.9,40.2-534.1V-4780H4022h1876v474.8c0,545.6,5.7,568.6,164.6,637.5c97.7,44.1,174.2,36.4,262.3-24.9c95.7-67,99.5-90,109.1-599.2l9.6-478.6l67,5.7c84.2,9.6,296.7,74.7,382.9,118.7c310.1,158.9,547.5,474.8,620.3,828.9c40.2,195.3,42.1,827,1.9,1018.4c-34.5,162.7-151.2,403.9-264.2,543.7l-84.3,105.3l-323.5,1.9c-268,1.9-350.4,9.6-476.7,44c-515,141.7-957.2,503.5-1186.9,970.6c-447.9,917-74.7,2015.8,838.5,2467.6l149.3,72.8l-5.7,932.3l-5.7,930.4l-49.8,137.8c-109.1,294.8-331.2,543.7-601.1,668.1c-214.4,97.6-271.8,103.4-1079.7,103.4h-744.7l-183.8,229.7c-101.5,124.4-201,237.4-222.1,248.9c-53.6,28.7-109.1-3.8-143.6-86.1c-47.9-120.6-103.4-99.6-415.4,158.9C2322.1,5054,2327.8,5050.1,2262.7,4985z"/><path d="M8721.7,945.8c-51.7-24.9-352.2-312-897.8-859.5l-823.2-825.1l-380.9,392.4c-210.6,216.3-405.8,403.9-434.6,419.2c-258.4,134-574.3-61.3-574.3-354.2c0-59.4,15.3-126.3,38.3-172.3c49.8-97.6,1060.5-1140.9,1148.6-1186.9c111-57.4,195.3-65.1,319.7-28.7c109.1,30.6,122.5,44,1083.5,1001.2c536,534.1,993.5,1005,1018.4,1047.1c91.9,155.1,78.5,333.1-32.5,461.3C9066.3,978.3,8880.6,1020.4,8721.7,945.8z"/></g></g></svg></button>`;
					buttonsContainer.innerHTML += `<button id="decline ${user.user_id}" class="decline_request" onclick="declineRequest(${user.user_id})"><svg  width="2em" height="2em" viewBox="0 0 1000 1000" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"  enable-background="new 0 0 1000 1000" xml:space="preserve"><g><g transform="translate(0.000000,512.000000) scale(0.100000,-0.100000)"><path d="M2885,4995.1c-38.3-30.6-40.2-166.5-11.5-874.7c11.5-224,9.6-386.6,0-405.8c-34.5-65.1-101.4-61.2-245,13.4c-130.2,68.9-137.8,68.9-183.8,40.2c-26.8-17.2-47.9-47.9-47.9-67c0-21.1,53.6-275.6,118.7-570.4l116.7-532.1l13.4-660.4l11.5-660.4l90-266.1c206.7-606.8,516.8-1037.4,945.6-1307.3c141.6-90,143.6-91.9,132.1-158.9c-5.7-36.4-11.5-86.1-11.5-107.2c0-40.2-11.5-42.1-290.9-51.7c-407.7-15.3-602.9-78.5-846-275.6C2525.1-1009.3,1526-2316.6,1439.8-2504.2c-93.8-206.7-114.8-342.6-114.8-792.4c0-562.7,45.9-738.8,256.5-1018.3c132.1-174.2,386.6-352.2,570.4-398.1l51.7-13.4l5.7,449.8c5.7,421.1,7.7,453.6,45.9,503.4c67,90,134,128.3,223.9,128.3c109.1,0,197.2-53.6,243.1-149.3c34.4-72.7,38.3-120.6,38.3-532.1V-4780h1875.8h1875.8v465.1c0,411.5,3.8,470.9,34.4,530.2c47.9,91.9,183.8,160.8,283.3,141.7c97.6-17.2,197.2-112.9,218.2-208.6c9.6-42.1,19.1-268,19.1-499.6v-424.9l130.2,24.9c342.6,65.1,668,308.2,821.1,610.6c120.6,237.3,126.3,273.7,135.9,763.7c5.7,375.2,1.9,480.4-24.9,597.2c-38.3,178-132.1,365.6-254.6,514.9l-91.9,114.8l-323.5,1.9c-373.2,1.9-507.2,30.6-786.7,160.8c-206.7,97.6-363.7,210.5-530.2,379c-170.4,172.3-248.8,285.2-350.3,493.8c-137.8,289-170.4,446-168.4,803.9c1.9,365.6,32.5,507.2,179.9,803.9c174.2,356,455.5,641.2,807.7,825l168.4,86.1v888.1c0,566.6-7.7,924.5-21,989.6c-11.5,55.5-55.5,174.2-97.6,264.1c-137.8,289-421.1,520.6-735,601c-97.6,24.9-246.9,30.6-872.8,30.6h-754.1L4110,4417.1c-103.4,132.1-204.8,243.1-224,250.7c-47.9,15.3-93.8-17.2-128.2-90c-23-49.8-44-67-88-70.8c-49.8-3.8-105.3,32.5-373.2,252.7C3122.3,4903.2,2967.3,5020,2950,5020C2934.7,5020,2906,5008.5,2885,4995.1z"/><path d="M6445.1,839.7c-176.1-76.6-266.1-298.6-193.3-472.8c15.3-36.4,174.2-210.5,354.1-390.5l327.3-325.4l-325.4-325.4c-199.1-199.1-335-354.1-354.1-396.2c-78.5-187.6,13.4-403.9,204.8-484.2c84.2-34.5,132.1-36.4,235.4-7.7c61.3,17.2,143.6,86.1,417.3,357.9L7450-867.6l340.7-336.9c336.9-335,396.2-379,520.6-379c181.8,0,361.8,179.9,363.7,359.8c0,124.4-53.6,199.1-388.5,534l-329.2,331.1L8296-19.7c346.4,350.3,379,398.1,379,541.7c-1.9,114.8-120.6,281.4-235.4,323.5c-76.6,30.6-195.2,26.8-277.5-7.7c-42.1-19.1-197.1-155-396.2-354.1l-325.4-325.4L7124.6,476c-189.5,191.4-346.4,333-392.4,354.1C6642.3,872.2,6527.4,876.1,6445.1,839.7z"/></g></g></svg></button>`;
				}
				listItem.appendChild(buttonsContainer);
				resultsContainer.appendChild(listItem);
			});
		})
		.catch(error => console.error('Error:', error));
	}, 300);
}

// Отправляем запрос на добавление пользователя в друзья
function addToFriendList(user_id) {
	fetch('/add_friend', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
		body: new URLSearchParams({
			request_type: 'add',
			user_id: user_id,
		}),
	})
	.then(response => response.json())
	.then(data => {
		console.log('Success:', data);

		// Если data.success не пустой, то значит запрос на добавление в друзья был успешно отправлен
		if (data.success != '') {
			// Меняем текст, класс и id кнопки на "Cancel request"
			document.getElementById(`add ${user_id}`).innerHTML = '<svg width="25px" height="25px" viewBox="0 0 1024 1024" class="icon"  version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M704 288h-281.6l177.6-202.88a32 32 0 0 0-48.32-42.24l-224 256a30.08 30.08 0 0 0-2.24 3.84 32 32 0 0 0-2.88 4.16v1.92a32 32 0 0 0 0 5.12A32 32 0 0 0 320 320a32 32 0 0 0 0 4.8 32 32 0 0 0 0 5.12v1.92a32 32 0 0 0 2.88 4.16 30.08 30.08 0 0 0 2.24 3.84l224 256a32 32 0 1 0 48.32-42.24L422.4 352H704a224 224 0 0 1 224 224v128a224 224 0 0 1-224 224H320a232 232 0 0 1-28.16-1.6 32 32 0 0 0-35.84 27.84 32 32 0 0 0 27.84 35.52A295.04 295.04 0 0 0 320 992h384a288 288 0 0 0 288-288v-128a288 288 0 0 0-288-288zM103.04 760a32 32 0 0 0-62.08 16A289.92 289.92 0 0 0 140.16 928a32 32 0 0 0 40-49.92 225.6 225.6 0 0 1-77.12-118.08zM64 672a32 32 0 0 0 22.72-9.28 37.12 37.12 0 0 0 6.72-10.56A32 32 0 0 0 96 640a33.6 33.6 0 0 0-9.28-22.72 32 32 0 0 0-10.56-6.72 32 32 0 0 0-34.88 6.72A32 32 0 0 0 32 640a32 32 0 0 0 2.56 12.16 37.12 37.12 0 0 0 6.72 10.56A32 32 0 0 0 64 672z" /></svg>';
			document.getElementById(`add ${user_id}`).setAttribute('class','cancel_request');
			document.getElementById(`add ${user_id}`).setAttribute('onclick', `cancelRequest(${user_id})`);
			document.getElementById(`add ${user_id}`).setAttribute('id', `cancel ${user_id}`);
		}
	})
}

// Отправляем запрос на отмену запроса на добавление пользователя в друзья
function cancelRequest(user_id) {
	fetch('/add_friend', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
		body: new URLSearchParams({
			request_type: 'cancel',
			user_id: user_id,
		}),
	})
	.then(response => response.json())
	.then(data => {
		console.log('Success:', data);

		// Если data.success не пустой, то значит запрос на добавление в друзья был успешно отправлен
		if (data.success != '') {
			// Меняем текст, класс и id кнопки на "Add to friend list"
			document.getElementById(`cancel ${user_id}`).innerHTML = '<svg class="icon" width="2em" height="2em" viewBox="0 0 1000 1000" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"  enable-background="new 0 0 1000 1000" xml:space="preserve"><g><g transform="translate(0.000000,512.000000) scale(0.100000,-0.100000)"><path d="M2704.2,4987.1c-34.5-34.5-36.4-57.4-28.7-245.1c24.9-505.5,34.5-988,23-1020.6c-24.9-68.9-95.7-65.1-245.1,9.6c-130.2,65.1-139.8,67-183.8,38.3c-24.9-15.3-46-46-46-67c0-21.1,53.6-281.5,118.7-580.2l118.7-540l11.5-651l11.5-651l90-268.1c162.8-478.7,344.7-781.2,633.8-1058.9c86.2-82.4,222.1-191.5,304.4-243.2l149.4-93.8l-13.4-97.6c-5.7-51.7-15.3-101.5-19.1-107.2c-3.8-7.6-134-17.2-289.1-23c-162.7-5.8-327.4-23-388.7-40.2c-162.8-45.9-361.9-155.1-484.4-266.1c-151.3-137.9-1106.7-1401.6-1192.9-1577.8c-97.7-199.1-122.5-365.7-122.5-802.3c0-430.8,24.9-597.4,124.5-802.3c74.7-155.1,183.8-293,321.7-405.9c99.6-82.3,291-187.6,382.9-208.7l51.7-11.5v407.8c0,226,9.6,442.3,19.2,480.6c24.9,88.1,126.4,178.1,218.3,195.3c107.2,21.1,227.8-44.1,277.6-149.4c36.4-74.7,40.2-114.9,40.2-534.2V-4780h1876.4h1876.4v474.9c0,434.6,3.8,478.7,38.3,534.2c74.7,124.5,201,162.8,333.2,103.4c158.9-68.9,164.7-91.9,164.7-637.6V-4780l63.2,11.5c285.3,49.8,520.8,170.4,704.6,365.7c147.4,157,208.7,256.6,279.6,457.6c53.6,149.4,53.6,155.1,53.6,630c0,409.8-5.7,494-34.5,591.7c-51.7,164.7-132.1,314-243.2,453.8l-97.6,120.6l-329.4,1.9c-298.7,1.9-344.6,7.6-497.8,53.6c-698.9,214.5-1166.1,723.8-1319.3,1439.9c-40.2,189.6-28.7,562.9,21.1,765.9c49.8,195.3,155.1,432.7,264.2,597.4c164.7,248.9,497.8,536.1,752.5,647.2c47.9,21.1,91.9,46,99.6,57.4c7.6,9.6,15.3,394.4,13.4,852.1c0,917.2-9.6,1041.6-109.1,1250.3c-151.3,323.6-419.3,545.7-760.2,635.7c-91.9,23-250.8,28.7-871.2,30.6h-756.3l-170.4,220.2c-93.8,120.6-189.6,233.6-214.5,248.9c-57.4,38.3-113,9.6-151.3-78.5c-24.9-63.2-51.7-78.5-122.5-67c-15.3,1.9-122.5,82.3-239.3,180C2771.2,5052.2,2769.3,5052.2,2704.2,4987.1z"/><path d="M7154.1,1209.3c-93.8-34.5-160.8-90-206.8-174.2c-40.2-76.6-42.1-107.2-47.9-553.4l-7.7-472.9L6409.2,3c-474.8-5.7-484.4-5.7-551.4-51.7C5608.9-221,5645.3-575.2,5922.9-692c57.4-23,158.9-28.7,520.8-28.7h448l7.7-472.9c5.7-517,9.6-534.2,124.5-639.5c80.4-76.6,126.4-93.8,239.3-93.8c124.5,0,212.5,42.1,291.1,139.8l59.3,74.7l5.7,495.9l5.7,495.9h459.5c490.2,0,545.7,9.6,647.2,101.5c61.3,57.4,116.8,180,116.8,262.3c0,134-113,296.8-235.5,342.7c-32.6,13.4-237.4,21.1-520.8,21.1h-467.2l-5.7,494c-5.7,492.1-5.7,495.9-53.6,564.9c-55.5,82.3-208.7,166.6-294.9,164.7C7238.3,1230.4,7186.6,1220.8,7154.1,1209.3z"/></g></g></svg>';
			document.getElementById(`cancel ${user_id}`).setAttribute('class','add');
			document.getElementById(`cancel ${user_id}`).setAttribute('onclick', `addToFriendList(${user_id})`);
			document.getElementById(`cancel ${user_id}`).setAttribute('id', `add ${user_id}`);
		}
	})
}

// Отправляем запрос на принятие запроса на добавление пользователя в друзья
function acceptRequest(user_id) {
	fetch('/add_friend', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
		body: new URLSearchParams({
			request_type: 'accept',
			user_id: user_id,
		}),
	})
	.then(response => response.json())
	.then(data => {
		console.log('Success:', data);

		// Если data.success не пустой, то значит запрос на добавление в друзья был успешно отправлен
		if (data.success != '') {
			// Удаляем кнопку "Accept request"
			document.getElementById(`accept ${user_id}`).remove();

			// Удаляем кнопку "Decline request"
			document.getElementById(`decline ${user_id}`).remove();
		}
	})
}

// Отправляем запрос на отклонение запроса на добавление пользователя в друзья
function declineRequest(user_id) {
	fetch('/add_friend', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
		body: new URLSearchParams({
			request_type: 'decline',
			user_id: user_id,
		}),
	})
	.then(response => response.json())
	.then(data => {
		console.log('Success:', data);

		// Если data.success не пустой, то значит запрос на добавление в друзья был успешно отправлен
		if (data.success != '') {
			// Удаляем кнопку "Accept request"
			document.getElementById(`accept ${user_id}`).remove();

			// Меняем текст, класс и id кнопки на "Add to friend list"
			document.getElementById(`decline ${user_id}`).innerHTML = 'Add to friend list';
			document.getElementById(`decline ${user_id}`).classList.remove('decline_request');
			document.getElementById(`decline ${user_id}`).classList.add('add');
			document.getElementById(`decline ${user_id}`).setAttribute('onclick', `addToFriendList(${user_id})`);
			document.getElementById(`decline ${user_id}`).setAttribute('id', `add ${user_id}`);
		}
	})
}

var current_chat_id = 0;
var current_user_id = 0;
var chat_name = '';

// Открытие личного чата с пользователем
function personalMessages(user_id, from, to) {
	if (from == undefined) {
		from = 0;
	}
	if (to == undefined) {
		to = 25;
	}

	// Отправляем запрос на открытие личного чата с пользователем
	fetch('/personal_messages', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
		body: new URLSearchParams({
			user_id: user_id,
			from: from,
			to: to,
		}),
	})
	.then(response => response.json())
	.then(data => {
		console.log('Success:', data);

		// Меняем название чата
		document.getElementById('chat_name').innerHTML = data.chat_name;
		chat_name = data.chat_name;

		// Очищаем предыдущие сообщения
		document.getElementById('chat_content').innerHTML = '';
		// Обновляем id чата
		current_chat_id = data.chat_id;

		// Обрабатываем сообщения
		// <div class="message mess_in" id="123456">
		// 	<div class="us_logo">
		// 		<img src="static/icons/us_logo.png" alt=""></img>
		// 	</div>
		// 	<div class="message_info">
		// 		<div class="name">Name Surname</div>
		// 		<div class="message_content">Hello world!</div>
		// 	</div>
		// </div>
		data.messages.forEach(message => {
			current_user_id = data.user_id;
			
			// Выводим сообщения в чат
			var messageContainer = document.createElement('div');

			// если входящее сообщение то класс mess_in, если исходящее то mess_out
			if (message.user_id == data.user_id) {
				messageContainer.classList.add('message', 'mess_out');
			}
			else {
				messageContainer.classList.add('message', 'mess_in');
			}
			messageContainer.setAttribute('id', message.message_id);
			var usLogo = document.createElement('div');
			usLogo.classList.add('us_logo');
			var usLogoImg = document.createElement('img');
			usLogoImg.setAttribute('src', 'static/icons/us_logo.png');
			usLogoImg.setAttribute('alt', '');
			usLogo.appendChild(usLogoImg);
			messageContainer.appendChild(usLogo);
			var messageInfo = document.createElement('div');
			messageInfo.classList.add('message_info');
			var name = document.createElement('div');
			name.classList.add('name');
			if (message.user_id == data.target_id) {
				name.innerHTML = data.chat_name;
			}
			else {
				name.innerHTML = data.user_name;
			}
			var messageContent = document.createElement('div');
			messageContent.classList.add('message_content');
			messageContent.innerHTML = message.content;
			messageInfo.appendChild(name);
			messageInfo.appendChild(messageContent);
			messageContainer.appendChild(messageInfo);
			document.getElementById('chat_content').appendChild(messageContainer);
		});
	})
}

// Подключение к сокету
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Выводим полученное сообщение в чат
socket.on('message', function(msg) {
	console.log('Received message', msg);
	var messageContainer = document.createElement('div');

	// если входящее сообщение то класс mess_in, если исходящее то mess_out
	if (msg.user_id == current_user_id) {
		messageContainer.classList.add('message', 'mess_out');
	}
	else {
		messageContainer.classList.add('message', 'mess_in');
	}
	messageContainer.setAttribute('id', msg.message_id);
	var usLogo = document.createElement('div');
	usLogo.classList.add('us_logo');
	var usLogoImg = document.createElement('img');
	usLogoImg.setAttribute('src', 'static/icons/us_logo.png');
	usLogoImg.setAttribute('alt', '');
	usLogo.appendChild(usLogoImg);
	messageContainer.appendChild(usLogo);
	var messageInfo = document.createElement('div');
	messageInfo.classList.add('message_info');
	var name = document.createElement('div');
	name.classList.add('name');
	console.log(current_user_id);
	if (msg.user_id == current_user_id) {
		name.innerHTML = msg.user_name;
	}
	else {
		name.innerHTML = chat_name;
	}
	var messageContent = document.createElement('div');
	messageContent.classList.add('message_content');
	messageContent.innerHTML = msg.content;
	messageInfo.appendChild(name);
	messageInfo.appendChild(messageContent);
	messageContainer.appendChild(messageInfo);
	document.getElementById('chat_content').appendChild(messageContainer);
});

// Отправка сообщения в чат
function sendMessage() {
	var message = document.getElementById('chat_input_message').value;
	var packet = {
		'chat_id': current_chat_id,
		'message': message,
	};
	socket.emit('message', packet);
}

// function toggleButton(clickedButton) {
// 	var buttons = document.querySelectorAll('.btn_for_sf');
// 	buttons.forEach(function(button){
// 		if (button === clickedButton){
// 			button.classList.add('active');
// 		}else {
// 			button.classList.remove('active');
// 		}
// 	})
// }

// Открытие и закрытие панели друзей
function toggleButtons(activeButton) {
	var additionalSection = document.getElementById('FRIENDS');
	var buttons = document.querySelectorAll('.btn_for_sf');

	buttons.forEach(function(button,index) {
		if (index + 1 === activeButton) {
			button.classList.add('active');
		}else{
			button.classList.remove('active');
		}
	});
	if (activeButton===1) {
		additionalSection.classList.remove('ON');
	}
	else {
		additionalSection.classList.add('ON');

		// Делаем запрос на получение списка друзей
		fetch('/friend_list', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			}
		})
		.then(response => response.json())
		.then(data => {
			console.log('Success:', data);

			// Очищаем предыдущие данные
			document.getElementById('FRIENDS').innerHTML = '';

			// Обрабатываем полученные данные
			// Список запросов на добавление в друзья
			data.invites.forEach(request => {
				// <div class="friend">
				// 	<div class="friend_logo">
				// 		<img src="static/icons/us_logo.png" alt=""></img>
				// 	</div>
				// 	<div class="friend_name">Name Surname</div>
				// </div>
				var friendContainer = document.createElement('div');
				friendContainer.classList.add('request');

				// us_logo
				var friendLogo = document.createElement('div');
				friendLogo.classList.add('us_logo');
				var friendLogoImg = document.createElement('img');
				friendLogoImg.setAttribute('src', 'static/icons/us_logo.png');
				friendLogoImg.setAttribute('alt', '');
				friendLogo.appendChild(friendLogoImg);
				friendContainer.appendChild(friendLogo);
				
				// us_name
				var friendName = document.createElement('div');
				friendName.classList.add('us_name');
				friendName.innerHTML = request.name + ' ' + request.surname;
				friendContainer.appendChild(friendName);
				
				// buttons
				var buttonsContainer = document.createElement('div');
				buttonsContainer.classList.add('buttons');
				
				// accept
				var acceptButton = document.createElement('button');
				acceptButton.classList.add('accept');
				acceptButton.setAttribute('onclick', `acceptRequest(${request.user_id})`);
				acceptButton.innerHTML = '✔';
				buttonsContainer.appendChild(acceptButton);

				// decline
				var declineButton = document.createElement('button');
				declineButton.classList.add('decline');
				declineButton.setAttribute('onclick', `declineRequest(${request.user_id})`);
				declineButton.innerHTML = '✖';
				buttonsContainer.appendChild(declineButton);

				// pm
				var writeButton = document.createElement('button');
				writeButton.classList.add('pm');
				writeButton.setAttribute('onclick', `personalMessages(${request.user_id})`);
				writeButton.innerHTML = '<svg class="pm_icon" width="2em" height="2em" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M23.7994 18.3704L23.8013 18.373C24.1307 18.8032 24.2888 20.2316 22.0258 19.9779C21.3596 19.9033 20.4282 19.7715 19.3088 19.3471C18.5551 19.0613 17.8986 18.7026 17.3584 18.3522C16.4699 18.7098 15.5118 18.9296 14.5113 18.9857C13.1436 20.8155 10.9602 22 8.50001 22C7.69152 22 6.91135 21.8717 6.17973 21.6339C5.74016 21.8891 5.24034 22.1376 4.68789 22.3471C3.56851 22.7715 2.63949 22.9297 1.97092 22.9779C1.47028 23.014 1.11823 22.9883 0.944098 22.9681C0.562441 22.9239 0.219524 22.7064 0.072134 22.3397C-0.0571899 22.0179 -0.0104055 21.6519 0.195537 21.3728C0.448192 21.0283 0.680439 20.6673 0.899972 20.3011C1.32809 19.5868 1.74792 18.8167 1.85418 17.9789C1.30848 16.9383 1.00001 15.7539 1.00001 14.5C1.00001 11.5058 2.75456 8.92147 5.29159 7.71896C6.30144 3.85296 9.81755 1 14 1C18.9706 1 23 5.02944 23 10C23 11.3736 22.6916 12.6778 22.1395 13.8448C21.9492 15.5687 22.8157 17.0204 23.7994 18.3704ZM7.00001 10C7.00001 6.13401 10.134 3 14 3C17.866 3 21 6.13401 21 10C21 11.1198 20.7378 12.1756 20.2723 13.1118C20.2242 13.2085 20.1921 13.3124 20.1772 13.4194C19.9584 14.9943 20.3278 16.43 21.0822 17.8083C19.9902 17.5451 18.9611 17.0631 18.0522 16.4035C17.7546 16.1875 17.3625 16.1523 17.0312 16.3117C16.1152 16.7525 15.0879 17 14 17C10.134 17 7.00001 13.866 7.00001 10ZM5.00353 10.2543C5.11889 14.4129 8.05529 17.8664 11.9674 18.7695C11.0213 19.5389 9.8145 20 8.50001 20C7.7707 20 7.07689 19.8586 6.44271 19.6026C6.14147 19.481 5.79993 19.5133 5.52684 19.6892C5.08797 19.972 4.56616 20.2543 3.9788 20.477C3.58892 20.6248 3.23263 20.7316 2.91446 20.8083C3.24678 20.2012 3.58332 19.4779 3.73844 18.7971C3.81503 18.461 3.8572 18.1339 3.87625 17.8266C3.88848 17.6293 3.84192 17.4327 3.74245 17.2618C3.27058 16.451 3.00001 15.5086 3.00001 14.5C3.00001 12.7904 3.78 11.263 5.00353 10.2543Z"/></svg></button></div>';
				buttonsContainer.appendChild(writeButton);
				friendContainer.appendChild(buttonsContainer);
				document.getElementById('FRIENDS').appendChild(friendContainer);
			});

			// Список друзей
			data.friends.forEach(friend => {
				// <div class="friend">
				// 	<div class="friend_logo">
				// 		<img src="static/icons/us_logo.png" alt=""></img>
				// 	</div>
				// 	<div class="friend_name">Name Surname</div>
				// </div>
				var friendContainer = document.createElement('div');
				friendContainer.classList.add('friend');

				// us_logo
				var friendLogo = document.createElement('div');
				friendLogo.classList.add('us_logo');
				var friendLogoImg = document.createElement('img');
				friendLogoImg.setAttribute('src', 'static/icons/us_logo.png');
				friendLogoImg.setAttribute('alt', '');
				friendLogo.appendChild(friendLogoImg);
				friendContainer.appendChild(friendLogo);
				
				// us_name
				var friendName = document.createElement('div');
				friendName.classList.add('us_name');
				friendName.innerHTML = friend.name + ' ' + friend.surname;
				friendContainer.appendChild(friendName);
				
				// buttons
				var buttonsContainer = document.createElement('div');
				buttonsContainer.classList.add('buttons');
				
				// delete
				var deleteButton = document.createElement('button');
				deleteButton.classList.add('delete');
				deleteButton.setAttribute('onclick', `deleteFriend(${friend.user_id})`);
				deleteButton.innerHTML = '🗑';
				buttonsContainer.appendChild(deleteButton);

				// pm
				var writeButton = document.createElement('button');
				writeButton.classList.add('pm');
				writeButton.setAttribute('onclick', `personalMessages(${friend.user_id})`);
				writeButton.innerHTML = '<svg class="pm_icon" width="2em" height="2em" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M23.7994 18.3704L23.8013 18.373C24.1307 18.8032 24.2888 20.2316 22.0258 19.9779C21.3596 19.9033 20.4282 19.7715 19.3088 19.3471C18.5551 19.0613 17.8986 18.7026 17.3584 18.3522C16.4699 18.7098 15.5118 18.9296 14.5113 18.9857C13.1436 20.8155 10.9602 22 8.50001 22C7.69152 22 6.91135 21.8717 6.17973 21.6339C5.74016 21.8891 5.24034 22.1376 4.68789 22.3471C3.56851 22.7715 2.63949 22.9297 1.97092 22.9779C1.47028 23.014 1.11823 22.9883 0.944098 22.9681C0.562441 22.9239 0.219524 22.7064 0.072134 22.3397C-0.0571899 22.0179 -0.0104055 21.6519 0.195537 21.3728C0.448192 21.0283 0.680439 20.6673 0.899972 20.3011C1.32809 19.5868 1.74792 18.8167 1.85418 17.9789C1.30848 16.9383 1.00001 15.7539 1.00001 14.5C1.00001 11.5058 2.75456 8.92147 5.29159 7.71896C6.30144 3.85296 9.81755 1 14 1C18.9706 1 23 5.02944 23 10C23 11.3736 22.6916 12.6778 22.1395 13.8448C21.9492 15.5687 22.8157 17.0204 23.7994 18.3704ZM7.00001 10C7.00001 6.13401 10.134 3 14 3C17.866 3 21 6.13401 21 10C21 11.1198 20.7378 12.1756 20.2723 13.1118C20.2242 13.2085 20.1921 13.3124 20.1772 13.4194C19.9584 14.9943 20.3278 16.43 21.0822 17.8083C19.9902 17.5451 18.9611 17.0631 18.0522 16.4035C17.7546 16.1875 17.3625 16.1523 17.0312 16.3117C16.1152 16.7525 15.0879 17 14 17C10.134 17 7.00001 13.866 7.00001 10ZM5.00353 10.2543C5.11889 14.4129 8.05529 17.8664 11.9674 18.7695C11.0213 19.5389 9.8145 20 8.50001 20C7.7707 20 7.07689 19.8586 6.44271 19.6026C6.14147 19.481 5.79993 19.5133 5.52684 19.6892C5.08797 19.972 4.56616 20.2543 3.9788 20.477C3.58892 20.6248 3.23263 20.7316 2.91446 20.8083C3.24678 20.2012 3.58332 19.4779 3.73844 18.7971C3.81503 18.461 3.8572 18.1339 3.87625 17.8266C3.88848 17.6293 3.84192 17.4327 3.74245 17.2618C3.27058 16.451 3.00001 15.5086 3.00001 14.5C3.00001 12.7904 3.78 11.263 5.00353 10.2543Z"/></svg></button></div>';
				buttonsContainer.appendChild(writeButton);
				friendContainer.appendChild(buttonsContainer);
				document.getElementById('FRIENDS').appendChild(friendContainer);
			});
		})
	}
}