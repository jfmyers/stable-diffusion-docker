import type { ActionFunction } from "@remix-run/node";
import { useActionData, Form, useTransition } from "@remix-run/react";

export const action: ActionFunction = async ({ request }) => {
  // console.log(request);
  const formData = await request.formData();
  const form = Object.fromEntries(formData);

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    prompt: form.description,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
  };

  const result = await fetch("http://44.211.96.130:8000/", requestOptions);
  const data = await result.json();
  return {
    image: data.image,
  };
};

export default function Index() {
  const actionData = useActionData();
  const transition = useTransition();

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", lineHeight: "1.4" }}>
      <div>
        {actionData && actionData.image && (
          <img
            alt="generated"
            src={`${actionData.image.replace("3.234.229.35", "44.211.96.130")}`}
            style={{ width: "512px", height: "512px" }}
          />
        )}
      </div>

      <div>
        <Form method="post" name="form">
          <fieldset disabled={transition.state === "submitting"}>
            <p>
              <label>
                Description:
                <br />
                <textarea name="description" />
              </label>
            </p>

            <p>
              <button type="submit">
                {transition.state === "submitting" ? "Creating..." : "Create"}
              </button>
            </p>
          </fieldset>
        </Form>
      </div>
    </div>
  );
}
