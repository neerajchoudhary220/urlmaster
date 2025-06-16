const base_url = "http://127.0.0.1:8090";
function fetchList() {
  $.ajax({
    method: "GET",
    url: `${base_url}/directory/`,
    success: function (response) {
      const directories = response.data.directories;
      const tbody = $("#directory-table tbody");
      tbody.empty();

      directories.forEach((dir, index) => {
        // Create <option> list with active branch selected
        const branchDropdown = `
    <select class="form-select form-select-sm w-75 branch-dropdown" data-path="${
      dir.path
    }">
        ${dir.git_branches
          .map(
            (branch) => `
                <option value="${branch.name}" ${
              branch.active ? "selected" : ""
            }>
                    ${branch.name}
                </option>
            `
          )
          .join("")}
    </select>
`;

        const row = `
                    <tr>
                        <th scope="row">${index + 1}</th>
                        <td>${dir.name}</td>
                        <td>${branchDropdown}</td>
                        <td>
                            <div class="btn-group">
                                <button class="btn btn-sm btn-outline-primary">Generate URL</button>
                            </div>
                        </td>
                    </tr>
                `;

        tbody.append(row);
      });
    },
    error: function (err) {
      console.error("Failed to load directories:", err);
    },
  });
}

$(document).ready(function () {
  fetchList(); //Fetch list data

  //click to Add Parent Directory Button
  $("#add_parent_directory_btn").on("click", function () {
    $(this).addClass("d-none");
    $("#add_parent_directory_group").removeClass("d-none");
  });

  //Add parent directory
  $("#add").on("click", function () {
    const data_ = {
      path: $("#parent_directory_path").val(),
      status: 1,
    };
    $.ajax({
      url: `${base_url}/directory/`,
      method: "post",
      data: JSON.stringify(data_),
      contentType: "application/json",
      success: function (response) {
        alert("Successfully saved");
      },
      error: function (xhr) {
        if (xhr.responseJSON && xhr.responseJSON.detail) {
          const error_msg = xhr.responseJSON.detail;
          alert(error_msg);
        } else {
        }
      },
    });
  });

  // Change branch event delegation
  $(document).on("change", ".branch-dropdown", function (e) {
    // Example: get selected value and data-path attribute
    const selectedBranch = $(this).val();
    const directoryPath = $(this).data("path");
    $.ajax({
      method: "get",
      url: `${base_url}/git/switch/?path=${directoryPath}&branch=${selectedBranch}`,
      success: function (response) {
        alert(response.msg);
      },
      error: function (xhr) {
        if (xhr.responseJSON && xhr.responseJSON.detail) {
          console.error(xhr.responseJSON);
          const error_msg = xhr.responseJSON.detail;
          alert(error_msg);
          window.location.reload();
        } else {
        }
      },
    });
  });
});
