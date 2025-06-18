const base_url = "http://127.0.0.1:8090";
const open_parent_dir = $("#open-parent-dir");
const getHerdLink = (selector) => {
  return selector.data("herd_link");
};
const copyLink = (contents) => {
  // Create a temporary input element
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val(`${contents}`).select();
  document.execCommand("copy");
  $temp.remove();
  alert("Text copied to clipboard!");
};
function fetchList() {
  $.ajax({
    method: "GET",
    url: `${base_url}/directory/`,
    success: function (response) {
      const directories = response.data.directories;
      const tbody = $("#directory-table tbody");
      tbody.empty();

      directories.forEach((dir, index) => {
        open_parent_dir
          .attr("data-dir_path", dir.parent_dir)
          .text(dir.parent_dir_name);
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
        const directory = `<div class="d-flex justify-content-start"><div class="me-auto"><span style="cursor:pointer;" class="text-primary open-directory" data-dir_path="${dir.path}">${dir.name}</span> <i class="fa fa-folder-open text-warning"></i></div> <button class="btn btn-sm btn-secondary text-white clone-directory-btn" data-dir_path="${dir.path}"><i class="fa fa-clone text-white"></i> Clone</button></div>`;
        const herd_link = dir.herd_link
          ? `<div class="d-flex justify-content-start"><a href="${dir.herd_link}" target="_blank" class="me-auto">${dir.herd_link}</a><button class="btn btn-sm btn-secondary copy-herd-link-btn"><i class="fa fa-clone"></i></button></div>`
          : `<button class="btn btn-primary text-white add-with-herd-btn" data-path="${dir.path}">Add Herd Link</button>`;
        let generate_url = "";

        if (dir.public_url) {
          generate_url = `<div class="d-flex justify-content-start"><a href="${dir.public_url}" target="_blank" class="me-auto">${dir.public_url}</a> <button class="btn btn-sm btn-secondary copy-public-url-btn"><i class="fa fa-clone"></i></button></div>`;
        } else if (dir.herd_link) {
          generate_url = `
    <div class="btn-group">
      <button class="btn btn-sm btn-outline-primary genereate-public-url-btn" data-herd_link="${dir.herd_link}">
        Generate Public URL
      </button>
    </div>`;
        } else {
          generate_url = `
    <div class="alert alert-danger p-0 p-1 mt-3 w-75" role="alert">
      Herd link is not available!
    </div>`;
        }
        const regenerate_public_url = dir.public_url
          ? `<button class="btn btn-info text-white regenerate-public-url-btn" data-bs-toggle="popover" data-bs-trigger="hover" title="Regenerate Public URL" data-herd_link="${dir.herd_link}"><i class="fa fa-exchange"></i></button>`
          : "--";
        const delete_public_url = dir.public_url
          ? `<button class="btn btn-danger ms-2 delete-url-btn text-white" data-herd_link="${dir.herd_link}"><i class="fa fa-trash text-white"></i></button>`
          : "";
        const row = `
                    <tr>
                        <th scope="row">${index + 1}</th>
                        <td>${directory}</td>
                        <td>${branchDropdown}</td>
                        <td>${herd_link}</td>
                        <td><div class="w-75">${generate_url}</div></td>
                        <td>
                          <div class='d-flex w-100'>${regenerate_public_url} ${delete_public_url}</div>
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

function generatePublicUrl(this_, herd_link) {
  $.ajax({
    method: "get",
    url: `${base_url}/cloudflared/?herd_link=${herd_link}`,
    beforeSend: function () {
      const waiting_msg = `<div class="alert alert-warning p-0 p-1 mt-3 w-75" role="alert">
 Please wait...
</div`;
      this_.addClass("d-none");
      this_.parent().html(waiting_msg);
    },
    success: function (response) {
      alert(response.msg);
    },

    error: function (xhr) {
      if (xhr.responseJSON && xhr.responseJSON.detail) {
        const error_msg = xhr.responseJSON.detail;
        alert(error_msg);
      }
    },
    complete: function () {
      window.location.reload();
    },
  });
}

$(document).ready(function () {
  fetchList(); //Fetch list data

  //click to Add Parent Directory Button
  $("#add_parent_directory_btn").on("click", function () {
    $(this).parent().addClass("d-none");
    $("#add_parent_directory_group").removeClass("d-none");
  });

  //Click To Close Parent Dir Btn
  $("#close-add-parent-dir").on("click", function () {
    $("#add_parent_directory_group").addClass("d-none");
    $("#add_parent_directory_btn").parent().removeClass("d-none");
  });

  //Add parent directory
  $("#add").on("click", function () {
    const data_ = {
      path: $("#parent_directory_path").val(),
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

  //Add with Herd
  $(document).on("click", ".add-with-herd-btn", function () {
    const dir_path = $(this).data("path");

    $.ajax({
      method: "get",
      url: `${base_url}/herd/?directory_path=${dir_path}`,

      success: function (response) {
        alert(response.msg);
      },
      error: function (xhr) {
        if (xhr.responseJSON && xhr.responseJSON.detail) {
          const error_msg = xhr.responseJSON.detail;
          alert(error_msg);
        }
      },
      complete: function () {
        window.location.reload();
      },
    });
  });

  //Generate Public URL
  $(document).on("click", ".genereate-public-url-btn", function () {
    const this_ = $(this);
    generatePublicUrl(this_, getHerdLink(this_));
  });

  //Regenerate Public URL
  $(document).on("click", ".regenerate-public-url-btn", function () {
    const this_ = $(this);
    generatePublicUrl(this_, getHerdLink(this_));
  });

  //delete Public URL
  $(document).on("click", ".delete-url-btn", function () {
    const this_ = $(this);
    $.ajax({
      method: "DELETE",
      url: `${base_url}/cloudflared/?herd_link=${getHerdLink(this_)}`,
      beforeSend: function () {
        const waiting_msg = `<div class="alert alert-warning p-0 p-1 mt-3 w-75" role="alert">
 Please wait...
</div`;
        this_.addClass("d-none");
        this_.parent().html(waiting_msg);
      },
      success: function (response) {
        alert(response.msg);
      },
      error: function (xhr) {
        if (xhr.responseJSON && xhr.responseJSON.detail) {
          const error_msg = xhr.responseJSON.detail;
          alert(error_msg);
        }
      },
      complete: function () {
        window.location.reload();
      },
    });
  });

  //clone directory
  $(document).on("click", ".clone-directory-btn", function () {
    const dir_path = $(this).data("dir_path");
    $("#dir_path").val(dir_path);
    $("#cloneDirectoryModal").modal("show");
  });

  $("#clone_dir_form").on("submit", function (e) {
    e.preventDefault(); // Prevent the default form submission
    let newDirName = $("#new_dir_name").val(); // Get input value
    const dir_path = $("#dir_path").val();

    $.ajax({
      method: "GET",
      url: `${base_url}/directory/clone/?directory_path=${dir_path}&new_folder_name=${newDirName}`,
      success: function (response) {
        alert(response.msg);
      },
      error: function (xhr) {
        if (xhr.responseJSON && xhr.responseJSON.detail) {
          const error_msg = xhr.responseJSON.detail;
          alert(error_msg);
        }
      },
      complete: function () {
        window.location.reload();
      },
    });
  });

  //Open Directory
  $(document).on("click", ".open-directory,#open-parent-dir", function () {
    const path = $(this).data("dir_path");
    $.ajax({
      method: "GET",
      url: `${base_url}/directory/open/?path=${path}`,
      success: function (response) {
        // alert(response.msg);
      },
      error: function (xhr) {
        if (xhr.responseJSON && xhr.responseJSON.detail) {
          const error_msg = xhr.responseJSON.detail;
          alert(error_msg);
        }
      },
      complete: function () {},
    });
  });

  $(document).on(
    "click",
    ".copy-herd-link-btn, .copy-public-url-btn",
    function () {
      copyLink($(this).parent().find("a").text());
    }
  );
});
