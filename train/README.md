## Bringing up a Jupyter instance

1. Create a VM compute instance using `main.ipynb`
2. SSH into the instance
3. Bring up container:
```
docker compose -f MLOPs-Project/train/docker-compose.yaml up -d
```
4. Get token and open Jupyter instance in browser
5. Open the "work" directory
6. Write code inside that directory
7. Before you delete your instance, inside the VM host (inside SSH session, not inside the Jupyter notebook container)

 * `cd` to `MLOps-Project`
 * authenticate to Github
 * do `git add` on each file that needs to be pushed to Github, then `git commit` and `git push`
