function doGet(e) { 
  Logger.log( JSON.stringify(e) );  // view parameters
  var result = 'Ok'; // assume success
  if (e.parameter == 'undefined') {
    result = 'No Parameters';
  }
  else {
	var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Database");
    var newRow = sheet.getLastRow() + 1;						
    var rowData = [];
    d=new Date();
    rowData[0] = d; // Timestamp in column A
    rowData[1] = d.toLocaleTimeString(); // Timestamp in column B
    
    for (var param in e.parameter) {
      Logger.log('In for loop, param=' + param);
      var value = stripQuotes(e.parameter[param]);
      Logger.log(param + ':' + e.parameter[param]);
      switch (param) {
        case 'I02': 
          rowData[2] = value; 
          result = 'PV';
          break;
        case 'I03': 
          rowData[3] = value; 
          result += 'Ns';
          break;
        case 'I04': 
          rowData[4] = value; 
          result += 'Np';
          break;
        case 'I05': 
          rowData[5] = value; 
          result += 'G';
          break;
        case 'I06': 
          rowData[6] = value; 
          result += 'T';
          break;
        case 'I07': 
          rowData[7] = value; 
          result += 'Ang';
          break;
        case 'I08':
          rowData[8] = value;
          result += 'CV';
          break;
        case 'Q01':
          rowData[9] = value;
          result += 'Vcalc';
          break;
        case 'Q02': 
          rowData[10] = value;
          result += 'Vmeas';
          break;
        case 'Q03': 
          rowData[11] = value; 
          result += 'Icalc';
          break;
        case 'Q04': 
          rowData[12] = value; 
          result += 'Imeas';
          break;
        case 'Q13': 
          rowData[21] = value; 
          result += 'n';
          break;
        case 'Q14': 
          rowData[22] = value; 
          result += 'Iph';
          break;
        case 'Q15': 
          rowData[23] = value;
          result += 'Io';
          break;
        case 'Q16':
          rowData[24] = value; 
          result += 'Rs';
          break;
        case 'Q17':
          rowData[25] = value; 
          result += 'Rsh';
          break;
        case 'Q18':
          rowData[26] = value; 
          result += 'Mode';
          break;
        case 'Q19':
          rowData[27] = value; 
          result += 'SetTime';
          break;
        default:
          result = "unsupported parameter";
      }
    }
    // Calculate Power and Resistance based on the logged values of Voltage and current
    rowData[13] = rowData[9] * rowData[11]; // Calculated Power 
    rowData[14] = rowData[10] * rowData[12]; // Measured Power

    if (rowData[11] > 0 || rowData[12] > 0 ) {
      rowData[15] = rowData[9] / rowData[11]; // Calculated Resistance
      rowData[16] = rowData[10] / rowData[12]; // Measured Resistance 
    }
    else {
      rowData[15] = 0
      rowData[16] = 0
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