import streamlit as st
import pandas as pd

# Sample data for demonstration
data = {
    'IDs': [1, 2, 3],
    'Type': ['Type A', 'Type B', 'Type C'],
    'Issues': ['Issue 1', 'Issue 2', 'Issue 3']
}

def main():
    st.title("Custom HTML Popup on Table Row Click")

    # Display sample table
    table_data = pd.DataFrame(data)
    st.write(table_data)

    # Add a button to trigger the popup
    

    # HTML content for the popup
    html_content = """
    <div id="custom-popup" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); z-index: 9999;">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: white; padding: 20px;">
            <h2>Custom Popup Content</h2>
            <p id="popup-content">This is a custom popup triggered by clicking on a table row.</p>
            <button onclick="closePopup()">Close</button>
        </div>
    </div>
    <script>
        function openPopup() {
            document.getElementById("custom-popup").style.display = "block";
        }
        
        function closePopup() {
            document.getElementById("custom-popup").style.display = "none";
        }

        function handleRowClick(rowId, rowType, rowIssues) {
            openPopup();
            // Update popup content
            document.getElementById("popup-content").innerHTML = "<strong>ID:</strong> " + rowId + "<br><strong>Type:</strong> " + rowType + "<br><strong>Issues:</strong> " + rowIssues;
        }

        document.addEventListener("DOMContentLoaded", function () {
            var tableRows = document.querySelectorAll(".stDataFrame > tbody > tr");
            tableRows.forEach(function(row, index) {
                if (index !== 0) { // Skip header row
                    row.addEventListener("click", function() {
                        var cells = row.getElementsByTagName("td");
                        handleRowClick(cells[0].innerText, cells[1].innerText, cells[2].innerText);
                    });
                }
            });
        });
    </script>
    """

    # Inject the HTML content into the Streamlit app
    st.markdown(html_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
