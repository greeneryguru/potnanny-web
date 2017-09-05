 else {
                if (window.confirm("Are you sure you want to delete this object from the system?")) {          
                    $.post("/outlet/" + pk + "/delete",
                        {'csrfmiddlewaretoken': '{{ csrf_token }}'},
                        function(){location.reload(false);}
                    );
                }
            }
