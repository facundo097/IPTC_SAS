function doGet(e) { 
  Logger.log( JSON.stringify(e) );  // view parameters
  var result = 'Ok'; // assume success
  if (e.parameter == 'undefined') {
    result = 'No Parameters';
  }
  else {
    var sheet_id = '1APg_aHuZdDOMjJTQf6wpr_L8itCIcCIbvE0jGAKACTk'; 		// Spreadsheet ID
    var sheet = SpreadsheetApp.openById(sheet_id).getActiveSheet();		// get Active sheet
    var newRow = sheet.getLastRow() + 1;						
    var rowData = [];
    d=new Date();
    rowData[0] = d; // Timestamp in column A
    rowData[1] = d.toLocaleTimeString(); // Timestamp in column A
    
    for (var param in e.parameter) {
      Logger.log('In for loop, param=' + param);
      var value = stripQuotes(e.parameter[param]);
      Logger.log(param + ':' + e.parameter[param]);
      switch (param) {
        case 'I02': 
          rowData[2] = value; 
          result = 'Irradiance written';
          break;
        case 'I03': 
          rowData[3] = value; 
          result += 'Temperature written';
          break;
        case 'I04': 
          rowData[4] = value; 
          result += 'Incidence Angle written';
          break;
        case 'I05': 
          rowData[5] = value; 
          result += 'Solar panel written';
          break;
        case 'I06': 
          rowData[6] = value; 
          result += 'Array Rows written';
          break;
        case 'I07': 
          rowData[7] = value; 
          result += 'Array Columns written';
          break;
        case 'I08':
          rowData[8] = value;
          result += 'Control Variable written';
          break;
        case 'Q01':
          rowData[9] = value;
          result += 'Calculated Voltage written';
          break;
        case 'Q02': 
          rowData[10] = value;
          result += 'Measured Voltage written';
          break;
        case 'Q03': 
          rowData[11] = value; 
          result += 'Calculated Current written';
          break;
        case 'Q04': 
          rowData[12] = value; 
          result += 'Measured Current written';
          break;
        case 'Q05': 
          rowData[13] = value; 
          result += 'Calculated Power written';
          break;
        case 'Q06': 
          rowData[14] = value; 
          result += 'Measured Power written';
          break;
        case 'Q07': 
          rowData[15] = value; 
          result += 'Calculated Resistance written';
          break;
        case 'Q08': 
          rowData[16] = value; 
          result += 'Measured Resistance written';
          break;
        case 'Q13': 
          rowData[21] = value; 
          result += 'Diode Ideality Factor written';
          break;
        case 'Q14': 
          rowData[22] = value; 
          result += 'Photoelectric Current  written';
          break;
        case 'Q15': 
          rowData[23] = value;
          result += 'Diode Saturation Current written';
          break;
        case 'Q16':
          rowData[24] = value; 
          result += 'Series Resistance written';
          break;
        case 'Q17':
          rowData[25] = value; 
          result += 'Shunt Resistance written';
          break;
        case 'Q18':
          rowData[26] = value; 
          result += 'Mode written';
          break;
        case 'Q19':
          rowData[27] = value; 
          result += 'Set time written';
          break;
        default:
          result = "unsupported parameter";
      }
    }

    // Calculate and write relative percent errors for voltage, current and power
    if (rowData[9] > 0 || rowData[11] > 0 ) {
      rowData[13] = rowData[9] * rowData[11];   // P_calc
      rowData[15] = rowData[9] / rowData[11]; // R_calc
    }
    else {
      rowData[13] = 0
      rowData[15] = 0
    }

    // Calculate and write relative percent errors for voltage, current and power
    if (rowData[9] > 0 || rowData[11] > 0 || rowData[13] > 0 || rowData[15] > 0) {
      rowData[17] = 100 * Math.abs(rowData[9] - rowData[10]) / rowData[9];   // Err_V
      rowData[18] = 100 * Math.abs(rowData[11] - rowData[12]) / rowData[11]; // Err_I
      rowData[19] = 100 * Math.abs(rowData[13] - rowData[14]) / rowData[13]; // Err_P
      rowData[20] = 100 * Math.abs(rowData[15] - rowData[16]) / rowData[15]; // Err_P
    }
    else {
      rowData[15] = 0
      rowData[16] = 0
      rowData[17] = 0
    }


    Logger.log(JSON.stringify(rowData));
    // Write new row below
    var newRange = sheet.getRange(newRow, 1, 1, rowData.length);
    newRange.setValues([rowData]);   
  }
  // Return result of operation
  return ContentService.createTextOutput(result);
}
function stripQuotes( value ) {
  return value.replace(/^["']|['"]$/g, "");
}